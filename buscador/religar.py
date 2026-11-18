"""Reconhece arquivos que só mudaram de lugar (outra pasta ou outro disco) e mantém tudo o que já
foi feito com eles: miniaturas, palavras-chave, rostos e pessoas, texto da foto, fala, coleções.

Como reconhece: mesmo nome, mesmo tamanho, mesmo tipo e mesma data de modificação (até 2 s de
diferença, por causa dos discos FAT/exFAT). Nada disso exige abrir o arquivo. Se o registro
antigo já tem o hash rápido (início, meio e fim), ele também é conferido, lendo só 768 KB.

Dois casos:
- novos(): apareceu um arquivo que o catálogo não conhecia, e há um registro marcado como
  "sumiu" igual a ele. O registro antigo passa para o caminho novo e o novo sai do catálogo.
- sumidos(): um arquivo sumiu, mas já existe no catálogo um registro mais novo igual a ele em
  outro lugar (o caminho novo foi indexado antes do antigo). O registro antigo assume o lugar
  do novo, levando junto as palavras-chave, coleções e favorito que o novo já tinha.
"""
import os
from pathlib import Path

from .db import refresh_fts
from .media import thumb_path

_COLS = ("f.id, f.volume_id, f.relpath, f.name, f.kind, f.size, f.mtime, f.qhash, f.has_thumb, "
         "f.missing, v.serial")


def _row(conn, fid: int):
    return conn.execute(f"SELECT {_COLS} FROM files f JOIN volumes v ON v.id = f.volume_id WHERE f.id = ?",
                        (fid,)).fetchone()


def _twins(conn, r, missing: int, skip: set[int]) -> list:
    """Registros iguais a `r` (nome, tamanho, tipo, data), os do mesmo disco primeiro."""
    if r["mtime"] is None:
        return []
    rows = conn.execute(
        f"""SELECT {_COLS} FROM files f JOIN volumes v ON v.id = f.volume_id
            WHERE f.size = ? AND f.name = ? AND f.kind = ? AND ABS(f.mtime - ?) < 2
              AND f.missing = ? AND f.trashed = 0 AND f.id != ?""",
        (r["size"], r["name"], r["kind"], r["mtime"], missing, r["id"])).fetchall()
    rows = [c for c in rows if c["id"] not in skip]
    rows.sort(key=lambda c: (c["volume_id"] != r["volume_id"], -(c["has_thumb"] or 0), c["id"]))
    return rows


def _same_content(old, path: Path | None) -> bool:
    """Confere o hash rápido quando o registro antigo já tem um. Sem hash guardado, vale o nome,
    tamanho e data."""
    if not old["qhash"] or path is None:
        return True
    from .dupes import quick_hash
    try:
        return quick_hash(path, old["size"]) == old["qhash"]
    except OSError:
        return False


def _take_place(conn, old, new) -> None:
    """O registro antigo (com todo o trabalho feito) passa para o caminho do novo, que sai do catálogo."""
    from .dupes import merge_metadata
    from .faces import face_crop_path
    merge_metadata(conn, new["id"], old["id"])  # palavras-chave suas, favorito e coleções do novo
    for (face_id,) in conn.execute("SELECT id FROM faces WHERE file_id = ?", (new["id"],)).fetchall():
        face_crop_path(face_id).unlink(missing_ok=True)
    for frame in range(3):
        thumb_path(new["serial"], new["id"], frame).unlink(missing_ok=True)
    conn.execute("DELETE FROM speech_fts WHERE rowid IN (SELECT id FROM transcripts WHERE file_id = ?)",
                 (new["id"],))
    conn.execute("DELETE FROM rejected_tags WHERE file_id = ?", (new["id"],))
    conn.execute("DELETE FROM files_fts WHERE rowid = ?", (new["id"],))
    conn.execute("DELETE FROM files WHERE id = ?", (new["id"],))  # rostos, tags e vetores saem em cascata
    conn.execute("UPDATE files SET volume_id = ?, relpath = ?, name = ?, missing = 0 WHERE id = ?",
                 (new["volume_id"], new["relpath"], new["name"], old["id"]))
    if old["serial"] != new["serial"]:  # miniaturas ficam numa pasta por disco
        for frame in range(3):
            src = thumb_path(old["serial"], old["id"], frame)
            if src.exists():
                dest = thumb_path(new["serial"], old["id"], frame)
                dest.parent.mkdir(parents=True, exist_ok=True)
                os.replace(src, dest)
    refresh_fts(conn, old["id"])


def novos(conn, todo: list[tuple[int, Path, str]], fresh: set[int]) -> tuple[list[tuple[int, Path, str]], int]:
    """Para os arquivos que acabaram de entrar no catálogo (`fresh`), procura um registro "sumiu"
    igual. Devolve a lista de trabalho corrigida (sem os que foram religados, mais os registros
    antigos que ainda não tinham miniatura) e quantos foram religados."""
    if not fresh:
        return todo, 0
    used: set[int] = set()
    out, moved = [], 0
    for fid, path, kind in todo:
        new = _row(conn, fid) if fid in fresh else None
        old = None
        if new is not None:
            old = next((c for c in _twins(conn, new, 1, used) if _same_content(c, path)), None)
        if old is None:
            out.append((fid, path, kind))
            continue
        used.add(old["id"])
        _take_place(conn, old, new)
        moved += 1
        if not old["has_thumb"]:
            out.append((old["id"], path, kind))
    return out, moved


def sumidos(conn, gone: list[int]) -> int:
    """Para os arquivos que acabaram de sumir, procura um registro mais novo igual em outro lugar.
    Devolve quantos foram religados."""
    if not gone:
        return 0
    from .volumes import connected
    online = connected()
    used: set[int] = set()
    moved = 0
    for fid in gone:
        old = _row(conn, fid)
        if old is None or not old["has_thumb"]:
            continue  # registro que nem chegou a ser processado: não há o que aproveitar
        for new in _twins(conn, old, 0, used):
            if new["id"] < old["id"]:
                continue  # só um registro criado depois deste pode ser o mesmo arquivo em outro lugar
            info = online.get(new["serial"])
            path = Path(f"{info['letter']}:{new['relpath']}") if info else None
            if _same_content(old, path):
                used.add(new["id"])
                _take_place(conn, old, new)
                moved += 1
                break
    return moved
