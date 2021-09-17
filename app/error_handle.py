from collections import namedtuple

from flask import render_template


Error = namedtuple("Error", "title message")


def e403(e):
    return render_template(
        "error/error.html",
        error=Error(
            title=f"{e.code}",
            message="권한이 부족합니다."
        )
    ), e.code


def e404(e):
    return render_template(
        "error/error.html",
        error=Error(
            title=f"{e.code}",
            message="해당 페이지를 찾을 수 없습니다."
        )
    ), e.code


def e405(e):
    return render_template(
        "error/error.html",
        error=Error(
            title=f"{e.code}",
            message="잘못된 요청 방식 입니다."
        )
    ), e.code


def file_is_empty(e):
    return render_template(
        "error/error.html",
        error=Error(
            title="업로드 실패",
            message="비어있는 파일을 업로드 할 수 없습니다."
        )
    ), 400


def file_is_too_big(e):
    return render_template(
        "error/error.html",
        error=Error(
            title="업로드 실패",
            message="이 파일의 용량은 너무 커서 업로드 할 수 없습니다."
        )
    ), 400


def private_project(e):
    return render_template(
        "error/error.html",
        error=Error(
            title="비공개 프로젝트",
            message="비공개 프로젝트는 멤버만 확인 할 수 있습니다."
        )
    ), 403


def user_not_login(e):
    return render_template(
        "error/error.html",
        error=Error(
            title="로그인 필요",
            message="해당 페이지를 사용하려면 로그인해야 합니다."
        )
    ), 403
