import os,sys,pygame

def resource_path(relative_path):
    """PyInstaller에서 리소스를 찾을 수 있도록 경로 설정"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def load_image(file_name):
    """이미지를 로딩하고 오류 발생 시 경고 출력"""
    path = resource_path(os.path.join('pictures', file_name))
    try:
        return pygame.image.load(path)
    except pygame.error as e:
        print(f"이미지 로딩 실패: {file_name} - {e}")
        return None

def load_image_menu(file_name):
    """이미지를 로딩하고 오류 발생 시 경고 출력"""
    path = resource_path(os.path.join('menu', file_name))
    try:
        return pygame.image.load(path)
    except pygame.error as e:
        print(f"이미지 로딩 실패: {file_name} - {e}")
        return None

def load_sound(file_name):
    """사운드 파일(mp3 등) 로딩"""
    path = resource_path(os.path.join('pictures', file_name))
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"사운드 로딩 실패: {file_name} - {e}")
        return None
