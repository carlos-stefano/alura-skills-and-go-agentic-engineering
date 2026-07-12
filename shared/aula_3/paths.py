from pathlib import Path


def find_course_root(start_path=None):
    current = Path(start_path or Path.cwd()).resolve()

    for candidate in [current, *current.parents]:
        if (candidate / "target_project").is_dir():
            return candidate

    raise FileNotFoundError(
        "A raiz do curso não foi encontrada. "
        "Esperava-se uma pasta target_project/ em algum diretório ancestral."
    )


def get_course_paths(start_path=None):
    course_root = find_course_root(start_path)

    return {
        "course_root": course_root,
        "target_project": course_root / "target_project",
        "aula_3": course_root / "aula_3",
        "shared": course_root / "shared",
    }
