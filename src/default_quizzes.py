"""기본 퀴즈 데이터: Linux 10개, Docker 10개, Git 10개 (총 30개)."""

from src.quiz import Quiz


# 상수 리스트로 두지 않고 함수로 매번 새 리스트를 만들어 돌려준다.
# 게임 중 퀴즈를 삭제하거나 추가해도 이 원본 데이터는 바뀌지 않아,
# 파일이 없거나 손상되어 기본 데이터로 복구할 때 항상 처음 상태의 30개를 얻을 수 있다.
# 미션 요구사항에 따라 dict가 아닌 Quiz 클래스의 인스턴스로 생성한다.
def create_default_quizzes():
    return [
        # ---------- Linux ----------
        Quiz(
            "현재 작업 중인 디렉터리의 절대 경로를 출력하는 명령어는?",
            ["ls", "cd", "pwd", "mkdir"],
            3,
            "print working directory의 약자입니다.",
        ),
        Quiz(
            "디렉터리 안의 파일과 폴더 목록을 보여주는 명령어는?",
            ["ls", "cat", "cp", "mv"],
            1,
            "list의 약자입니다.",
        ),
        Quiz(
            "새 디렉터리를 만드는 명령어는?",
            ["touch", "rmdir", "cd", "mkdir"],
            4,
            "make directory의 약자입니다.",
        ),
        Quiz(
            "파일의 내용을 터미널에 출력하는 명령어는?",
            ["cd", "cat", "mkdir", "pwd"],
            2,
            "concatenate(이어 붙이다)에서 온 이름입니다.",
        ),
        Quiz(
            "파일이나 디렉터리를 다른 위치로 옮기거나 이름을 바꾸는 명령어는?",
            ["cp", "rm", "mv", "ln"],
            3,
            "move의 약자입니다.",
        ),
        Quiz(
            "파일의 권한(읽기·쓰기·실행)을 변경하는 명령어는?",
            ["chown", "chmod", "chgrp", "umask"],
            2,
            "change mode의 약자입니다.",
        ),
        Quiz(
            "파일 내용에서 특정 문자열이 들어 있는 줄을 찾는 명령어는?",
            ["find", "sort", "wc", "grep"],
            4,
            "정규 표현식으로 텍스트를 검색하는 명령어입니다.",
        ),
        Quiz(
            "현재 실행 중인 프로세스 목록을 확인하는 명령어는?",
            ["ps", "kill", "df", "du"],
            1,
            "process status의 약자입니다.",
        ),
        Quiz(
            "다른 명령어 앞에 붙여 그 명령을 관리자(root) 권한으로 실행하는 명령어는?",
            ["su", "sudo", "root", "admin"],
            2,
            "superuser do의 약자입니다.",
        ),
        Quiz(
            "권한 표기 rwxr-xr-x를 숫자로 나타낸 것은?",
            ["644", "700", "755", "777"],
            3,
            "r=4, w=2, x=1을 소유자·그룹·기타 사용자별로 더합니다.",
        ),
        # ---------- Docker ----------
        Quiz(
            "이미지로 새 컨테이너를 만들고 바로 실행하는 명령어는?",
            ["docker build", "docker run", "docker pull", "docker push"],
            2,
            "'실행하다'라는 뜻의 영어 단어입니다.",
        ),
        Quiz(
            "실행 중인 컨테이너 목록을 확인하는 명령어는?",
            ["docker images", "docker logs", "docker inspect", "docker ps"],
            4,
            "Linux에서 프로세스 목록을 보는 명령어와 이름이 같습니다.",
        ),
        Quiz(
            "Docker Hub 같은 레지스트리에서 이미지를 내려받는 명령어는?",
            ["docker pull", "docker push", "docker get", "docker load"],
            1,
            "'당겨 오다'라는 뜻의 영어 단어입니다.",
        ),
        Quiz(
            "Dockerfile을 읽어 이미지를 만드는 명령어는?",
            ["docker run", "docker create", "docker build", "docker start"],
            3,
            "'짓다, 만들다'라는 뜻의 영어 단어입니다.",
        ),
        Quiz(
            "Dockerfile에서 기반이 되는 베이스 이미지를 지정하는 명령어는?",
            ["RUN", "CMD", "FROM", "COPY"],
            3,
            "보통 Dockerfile의 맨 첫 줄에 작성합니다.",
        ),
        Quiz(
            "컨테이너의 80번 포트를 호스트의 8080번 포트로 연결하는 docker run 옵션은?",
            ["-p 8080:80", "-p 80:8080", "-v 8080:80", "-e 8080:80"],
            1,
            "-p 옵션은 '호스트 포트:컨테이너 포트' 순서로 씁니다.",
        ),
        Quiz(
            "컨테이너를 삭제해도 데이터를 유지하려면 무엇을 사용해야 할까?",
            ["이미지 태그", "환경 변수", "포트 매핑", "볼륨(Volume)"],
            4,
            "컨테이너 바깥에 데이터를 저장하는 공간입니다.",
        ),
        Quiz(
            "실행 중인 컨테이너 안에서 셸 등 추가 명령을 실행하는 명령어는?",
            ["docker run", "docker exec", "docker attach", "docker start"],
            2,
            "execute(실행하다)의 약자입니다.",
        ),
        Quiz(
            "이미지를 실행해 만들어진, 격리된 실행 환경을 무엇이라고 할까?",
            ["볼륨", "네트워크", "컨테이너", "레지스트리"],
            3,
            "물건을 담는 상자에 비유되는 이름입니다.",
        ),
        Quiz(
            "여러 컨테이너를 YAML 파일 하나로 정의하고 한 번에 실행하는 도구는?",
            ["Dockerfile", "Docker Hub", "Docker Volume", "Docker Compose"],
            4,
            "'구성하다'라는 뜻의 영어 단어가 들어갑니다.",
        ),
        # ---------- Git ----------
        Quiz(
            "현재 폴더를 새 Git 저장소로 만드는 명령어는?",
            ["git init", "git clone", "git start", "git new"],
            1,
            "initialize(초기화하다)의 약자입니다.",
        ),
        Quiz(
            "원격 저장소 전체를 로컬로 처음 복제해 오는 명령어는?",
            ["git pull", "git fetch", "git clone", "git copy"],
            3,
            "'복제'라는 뜻의 영어 단어입니다.",
        ),
        Quiz(
            "변경한 파일을 다음 커밋에 포함되도록 스테이징 영역에 올리는 명령어는?",
            ["git commit", "git add", "git push", "git status"],
            2,
            "'추가하다'라는 뜻의 영어 단어입니다.",
        ),
        Quiz(
            "스테이징된 변경 사항을 하나의 기록으로 저장하는 명령어는?",
            ["git save", "git push", "git log", "git commit"],
            4,
            "-m 옵션으로 메시지를 함께 남깁니다.",
        ),
        Quiz(
            "로컬 저장소의 커밋을 원격 저장소에 업로드하는 명령어는?",
            ["git pull", "git push", "git fetch", "git merge"],
            2,
            "'밀어 넣다'라는 뜻의 영어 단어입니다.",
        ),
        Quiz(
            "원격 저장소의 새 커밋을 가져와 현재 브랜치에 합치는 명령어는?",
            ["git pull", "git push", "git clone", "git add"],
            1,
            "'당겨 오다'라는 뜻의 영어 단어입니다.",
        ),
        Quiz(
            "새 브랜치를 만들면서 바로 그 브랜치로 이동하는 명령어는?",
            ["git branch -d", "git merge -b", "git checkout -b", "git switch -d"],
            3,
            "-b는 branch를 뜻하는 옵션입니다.",
        ),
        Quiz(
            "다른 브랜치의 변경 사항을 현재 브랜치에 합치는 명령어는?",
            ["git clone", "git init", "git log", "git merge"],
            4,
            "'합병하다'라는 뜻의 영어 단어입니다.",
        ),
        Quiz(
            "수정되거나 스테이징된 파일이 무엇인지 현재 상태를 확인하는 명령어는?",
            ["git log", "git status", "git show", "git tag"],
            2,
            "'상태'라는 뜻의 영어 단어입니다.",
        ),
        Quiz(
            "Git이 추적하지 않을 파일과 폴더를 적어 두는 파일은?",
            [".gitignore", ".gitkeep", ".gitconfig", ".gitattributes"],
            1,
            "'무시하다'라는 뜻의 영어 단어가 들어갑니다.",
        ),
    ]
