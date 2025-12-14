from email.policy import default
from struct import unpack
from tkinter import *
import time
import pygame
from PIL import Image, ImageTk
import os
import math


class MenuCanvas:
    def __init__(self,window):
        self.window = window
        self.canvas=Canvas(self.window, bg ="white") 
        self.keys = set()

        #메뉴캔버스 메뉴 배경, 선택 화살표 이미지
        menu_bg_path = os.path.join(os.path.dirname(__file__), "image", "menu_background.png")
        bg_img = Image.open(menu_bg_path)
        bg_img = bg_img.resize((1280, 960)) #배경
        self.menu_bg = ImageTk.PhotoImage(bg_img)

        # 캔버스에 배경 이미지 추가
        self.menuBackground = self.canvas.create_image(0, 0, anchor="nw", image=self.menu_bg, tags="Background")

        arrow_path = os.path.join(os.path.dirname(__file__), "image", "select_arrow.png")
        self.select_arrow = PhotoImage(file=arrow_path).subsample(20)
        self.selectImage = self.canvas.create_image(665,355, image = self.select_arrow, tags = "select")
        

        self.canvas.create_text(640,340, font ="Times 13 italic bold", fill="white", text="시작")              
        self.canvas.create_text(640,380, font ="Times 13 italic bold", fill="white", text="설정")
        self.canvas.create_text(640,420, font ="Times 13 italic bold", fill="white", text="종료")

        self.menu_index = 0 # 0 = 시작 / 1 = 설정 / 2 = 종료

    def display(self):
        pass

    def pack(self):
        self.canvas.pack(expand=True, fill=BOTH)
        
    def unpack(self):
        self.canvas.pack_forget()

    def keyPresseHandler(self, event):
        pass
            
    def keyPresseReleaseHandler(self, event):
        if (event.keycode == 38 or event.keycode == 87) and self.menu_index > 0: #위
            self.menu_index -= 1
            self.canvas.move(self.selectImage, 0, -40)
            return -1

        elif(event.keycode == 40 or event.keycode == 83) and self.menu_index < 2: #아래
            self.menu_index += 1
            self.canvas.move(self.selectImage, 0, 40)
            return -1
        elif event.keycode == 32 or event.keycode == 13: #스페이스 or 엔터로 선택
            if self.menu_index == 0:
                return 2 #스테이지
            elif self.menu_index == 1:
                return 1 #설정
            elif self.menu_index == 2:
                self.window.destroy() #종료

    def destroy(self):
        self.canvas.delete("all")
        self.canvas.destroy()    
    
class settingCanvas:
    def __init__ (self, window):
        self.window = window
        self.canvas = Canvas(self.window, bg ="white")
        self.keys = set()

        self.canvas.create_text(640, 200, text="설정", font="Times 20 bold")
        self.canvas.create_text(640, 300, text="BGM 볼륨", font="Times 14")
        # 난이도 텍스트은 아래에 표시
        self.canvas.create_text(640, 500, text="뒤로가기(ESC)", font="Times 14")
       
        # 세팅캔버스 선택 화살표, 볼륨조절 빈상자, 상자 생성
        arrow_path = os.path.join(os.path.dirname(__file__), "image", "select_arrow.png")
        self.select_arrow = PhotoImage(file=arrow_path).subsample(20)
        self.selectImage = self.canvas.create_image(680,320, image = self.select_arrow, tags = "select")

        empty_box_path = os.path.join(os.path.dirname(__file__), "image", "empty_box.png")
        self.empty_box = PhotoImage(file=empty_box_path).subsample(20)
        self.empty_box_image = self.canvas.create_image(100000,450, image = self.empty_box, tags = "empty_box")

        filled_box_path = os.path.join(os.path.dirname(__file__), "image", "filled_box.png")
        self.filled_box = PhotoImage(file=filled_box_path).subsample(20)
        self.filled_box_image = self.canvas.create_image(100000,470, image = self.filled_box, tags = "filled_box")

        # BGM 볼륨 바
        self.bgm_boxes = []
        self.create_volume_bar(self.bgm_boxes, start_x=525, y=330)

        # 난이도 인덱스: 0=쉬움,1=보통,2=어려움
        self.stage_level_index = 0
        self._difficulty_labels = ["쉬움", "보통", "어려움"]
        # 난이도 표시 텍스트 
        self.difficulty_label_id = self.canvas.create_text(620, 400, text="난이도 :", font="Times 14")
        self.difficulty_value_id = self.canvas.create_text(685, 400, text=self._difficulty_labels[self.stage_level_index], font="Times 14")

        # 설정 인덱스: 0 = bgm / 1 = 난이도 / 2 = 뒤로가기
        self.setting_index = 0
        self.bgm_balance_index = 5
        self.update_volume_bar(self.bgm_boxes, self.bgm_balance_index)

    # 사운드바 10칸 생성
    def create_volume_bar(self, box_list, start_x, y):
        for i in range(10):
            img = self.canvas.create_image(start_x + i * 25, y, image=self.empty_box)
            box_list.append(img)

    # 사운드바 업데이트
    def update_volume_bar(self, box_list, volume):
        for i in range(10):
            if i < volume:
                self.canvas.itemconfig(box_list[i], image=self.filled_box)
            else:
                self.canvas.itemconfig(box_list[i], image=self.empty_box)

    def display(self):
        pass

    def pack(self):
        self.canvas.pack(expand=True, fill=BOTH)
        
    def unpack(self):
        self.canvas.pack_forget()

    def keyPresseHandler(self, event):
        pass
            
    def keyPresseReleaseHandler(self, event):

        if (event.keycode == 38 or event.keycode == 87) and self.setting_index > 0: # 위
            self.setting_index -= 1
            self.canvas.move(self.selectImage, 0, -100)
            return -1

        elif (event.keycode == 40 or event.keycode == 83) and self.setting_index < 2: # 아래
            self.setting_index += 1
            self.canvas.move(self.selectImage, 0, 100)
            return -1

        elif event.keycode == 32 or event.keycode == 13: # 스페이스, 엔터
            if self.setting_index == 0: # bgm 선택
                self.bgm_balance_index += 1
                if self.bgm_balance_index == 11:
                    self.bgm_balance_index = 0
                self.update_volume_bar(self.bgm_boxes, self.bgm_balance_index)

            elif self.setting_index == 1: # 난이도 선택: 순환
                self.stage_level_index = (self.stage_level_index + 1) % 3
                # 표시 갱신
                try:
                    self.canvas.itemconfig(self.difficulty_value_id, text=self._difficulty_labels[self.stage_level_index])
                except Exception:
                    pass

            elif self.setting_index == 2: # 돌아가기
                return 0

        if event.keycode == 27:  # esc
            return 0

        return -1

    def destroy(self):
        self.canvas.delete("all")
        self.canvas.destroy()    


class Player:
    def __init__(self, images_r, images_l, start_x, start_y, speed=6, hp=100):
        self.images_r = images_r
        self.images_l = images_l
        self.world_x = start_x
        self.world_y = start_y
        self.speed = speed
        self.hp = hp

        # animation
        self.anim_r = 0
        self.anim_l = 0
        self.anim_counter = 0
        self.frame_delay = 5
        self.facing = "R"

        # canvas item id (생성은 draw 시)
        self.image_id = None

    def update(self, keys, world_w, world_h):
        dx = 0
        dy = 0
        moving = False

        # 상하
        if (38 in keys) or (87 in keys):  # Up / W
            dy = -self.speed
            moving = True
        elif (40 in keys) or (83 in keys):  # Down / S
            dy = self.speed
            moving = True

        # 좌우
        if (65 in keys) or (37 in keys):  # A / Left
            dx = -self.speed
            self.facing = "L"
            moving = True
        elif (68 in keys) or (39 in keys):  # D / Right
            dx = self.speed
            self.facing = "R"
            moving = True

        # 위치 갱신 (월드 경계 내)
        if dx != 0 or dy != 0:
            self.world_x = max(0, min(self.world_x + dx, world_w))
            self.world_y = max(0, min(self.world_y + dy, world_h))

         # 애니메이션
        if moving:
            self.anim_counter += 1
            if self.anim_counter % self.frame_delay == 0:
                if self.facing == "R":
                    self.anim_r = (self.anim_r + 1) % 3
                else:
                    self.anim_l = (self.anim_l + 1) % 3
        else:
            self.anim_counter = 0
            self.anim_r = 0
            self.anim_l = 0

    def draw(self, canvas, camera_x, camera_y):
        # 화면 좌표 계산
        screen_x = self.world_x - camera_x
        screen_y = self.world_y - camera_y

        # 현재 이미지 선택
        if self.facing == "R":
            img = self.images_r[self.anim_r]
        else:
            img = self.images_l[self.anim_l]

        if self.image_id is None:
            self.image_id = canvas.create_image(screen_x, screen_y, image=img, tags="Player")
        else:
            canvas.coords(self.image_id, screen_x, screen_y)
            canvas.itemconfig(self.image_id, image=img)

    def take_damage(self, amount):
        self.hp -= amount
        return self.hp > 0

    def get_world_pos(self):
        return (self.world_x, self.world_y)



class Enemy:
    def __init__(self, x, y, sprite=None, hp=50):
        self.world_x = x
        self.world_y = y
        self.hp = hp
        self.sprite = sprite  
        self.image_id = None
        self.contact_timer = 0
        self.attack_cooldown = 30  

        # 추적 관련 파라미터
        self.speed = 2.5
        self.follow_range = 800

    def update(self, player_world_pos, world_w, world_h):
        px, py = player_world_pos
        dx = px - self.world_x
        dy = py - self.world_y
        dist = math.hypot(dx, dy)

        if dist == 0 or dist > self.follow_range:
            return

        nx = dx / dist
        ny = dy / dist
        move = min(self.speed, dist)
        self.world_x += nx * move
        self.world_y += ny * move

        self.world_x = max(0, min(self.world_x, world_w))
        self.world_y = max(0, min(self.world_y, world_h))

    def draw(self, canvas, camera_x, camera_y):
        screen_x = self.world_x - camera_x
        screen_y = self.world_y - camera_y
        if self.sprite is not None:
            if self.image_id is None:
                self.image_id = canvas.create_image(screen_x, screen_y, image=self.sprite, tags="Enemy")
            else:
                canvas.coords(self.image_id, screen_x, screen_y)

    def take_damage(self, amount):
        self.hp -= amount
        return self.hp > 0



class StageCanvas:
    def __init__ (self, window):
        self.window = window
        # 뷰포트
        self.screen_w = 1280
        self.screen_h = 960
        self.screen_center_x = self.screen_w // 2
        self.screen_center_y = self.screen_h // 2

        self.canvas = Canvas(self.window, bg="white", width=self.screen_w, height=self.screen_h)
        self.keys = set()

        # 배경 로드
        stage_bg_path = os.path.join(os.path.dirname(__file__), "image", "forest_stage_bg.png")
        bg_img = Image.open(stage_bg_path)
        bg_img = bg_img.resize((2560, 1920))
        self.world_w, self.world_h = bg_img.size
        self.bg_photo = ImageTk.PhotoImage(bg_img)
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo, tags="Background")

        # 플레이어 스프라이트
        self.playerR = [PhotoImage(file=os.path.join(os.path.dirname(__file__), "image", f"player_right{i}.png")).subsample(5) for i in range(1, 4)]
        self.playerL = [PhotoImage(file=os.path.join(os.path.dirname(__file__), "image", f"player_left{i}.png")).subsample(5) for i in range(1, 4)]

        # Player 객체 (월드 중앙)
        start_x = self.world_w // 2
        start_y = self.world_h // 2
        self.player = Player(self.playerR, self.playerL, start_x, start_y, speed=6, hp=100)

        # 카메라 초기화
        self.camera_x = max(0, min(self.player.world_x - self.screen_center_x, self.world_w - self.screen_w))
        self.camera_y = max(0, min(self.player.world_y - self.screen_center_y, self.world_h - self.screen_h))

        self.facing = "R"

        # 적 스프라이트
        carrot_path = os.path.join(os.path.dirname(__file__), "image", "carrot_monster.png")
        self.carrot_sprite = PhotoImage(file=carrot_path).subsample(15) if os.path.exists(carrot_path) else None

        # 적 목록, 점수, 요청 플래그
        self.enemies = []
        self.score = 0
        self.request_scene = None

        # 적 스폰 관련
        self.MAX_ENEMIES = 20
        self._rand = __import__('random')

        # 적 속도 조정 파라미터 (스코어에 비례하여 증가)
        self.enemy_base_speed = 2.5        # 기본 속도
        self.enemy_speed_per_score = 0.1   # 스코어 1당 증가량
        self.enemy_max_speed = 10.0         # 최대 속도 상한

        # 난이도 관련: 기본은 쉬움(1히트)
        self.stage_level_index = 0  # 0 = 쉬움 / 1 = 보통 / 2 = 어려움
        self._difficulty_hp_map = {0: 1, 1: 2, 2: 3}
        self.enemy_initial_hp = self._difficulty_hp_map.get(self.stage_level_index, 1)

        # 적 피격 범위 확장 마진 (픽셀). 값 조정으로 범위 조절
        self.enemy_hit_margin = 105
        # 무기와 적 충돌은 훨씬 좁게 감지하도록 별도 마진 사용 (필요시 값 조절)
        self.weapon_hit_margin = 3        # 무기 히트 마진 (적용 범위)

        # 적 스폰
        self._spawn_enemies()

        # HUD
        self.hp_text_id = self.canvas.create_text(10, 10, anchor="nw", text=f"HP: {self.player.hp}", fill="white", font="Times 16 bold", tags="HUD")
        self.score_text_id = self.canvas.create_text(10, 34, anchor="nw", text=f"Score: {self.score}", fill="white", font="Times 16 bold", tags="HUD")

        # 플레이어 초기 이미지는 Player.draw에서 생성
        self.speed = 6

        # 무기(wepon.png) 로드 및 회전 관련 초기화
        wepon_path = os.path.join(os.path.dirname(__file__), "image", "wepon.png")
        if os.path.exists(wepon_path):
            self.weapon_orig = Image.open(wepon_path).convert("RGBA")
            self.weapon_orig = self.weapon_orig.resize((100, 100), Image.LANCZOS)
        else:
            self.weapon_orig = None

        # 무기 회전 속도
        self.weapon_angle = 0.0
        self.weapon_speed = 2.5
        self.weapon_radius = 110
        self.weapon_photo = None
        self.weapon_image_id = None
        self.weapon_active = True
        self.respawn_delay = 3000

    # 난이도 설정을 외부에서 적용할 때 호출
    def set_difficulty(self, level_index: int):
        try:
            level = int(level_index)
        except Exception:
            level = 0
        self.stage_level_index = max(0, min(2, level))
        self.enemy_initial_hp = self._difficulty_hp_map.get(self.stage_level_index, 1)
        # 기존 적들의 체력도 난이도에 맞게 맞춤(선택사항)
        for e in self.enemies:
            e.hp = self.enemy_initial_hp

    def _spawn_enemies(self):
        self.enemies.clear()
        sx = self.world_w // 2
        sy = self.world_h // 2
        if self.carrot_sprite is not None:
            self.enemies.append(Enemy(sx + 200, sy, sprite=self.carrot_sprite, hp=self.enemy_initial_hp))
            self.enemies.append(Enemy(sx - 300, sy + 100, sprite=self.carrot_sprite, hp=self.enemy_initial_hp))
            self.enemies.append(Enemy(sx + 400, sy - 80, sprite=self.carrot_sprite, hp=self.enemy_initial_hp))

    def _spawn_enemy_random(self):
        if len(self.enemies) >= self.MAX_ENEMIES:
            return
        margin = 100
        x = self._rand.randint(margin, max(margin + 1, self.world_w - margin))
        y = self._rand.randint(margin, max(margin + 1, self.world_h - margin))
        e = Enemy(x, y, sprite=self.carrot_sprite, hp=self.enemy_initial_hp)
        e.image_id = None
        e.contact_timer = 0
        e.speed = min(self.enemy_max_speed, self.enemy_base_speed + self.score * self.enemy_speed_per_score)
        self.enemies.append(e)

    def _schedule_enemy_respawn(self, x=None, y=None):
        def do_respawn():
            if len(self.enemies) < self.MAX_ENEMIES:
                if x is None or y is None:
                    self._spawn_enemy_random()
                else:
                    e = Enemy(x, y, sprite=self.carrot_sprite, hp=self.enemy_initial_hp)
                    e.image_id = None
                    e.contact_timer = 0
                    e.speed = min(self.enemy_max_speed, self.enemy_base_speed + self.score * self.enemy_speed_per_score)
                    self.enemies.append(e)
        self.canvas.after(self.respawn_delay, do_respawn)

    def _reactivate_weapon(self):
        self.weapon_active = True
        self.weapon_image_id = None
        self.weapon_photo = None

    def reset(self):
        self.clear_entities()
        self.player.hp = 100
        self.score = 0
        self.player.world_x = self.world_w // 2
        self.player.world_y = self.world_h // 2
        self._spawn_enemies()
        for e in self.enemies:
            e.image_id = None
            e.contact_timer = 0
            e.speed = min(self.enemy_max_speed, self.enemy_base_speed + self.score * self.enemy_speed_per_score)
            e.hp = self.enemy_initial_hp
        if getattr(self, 'hp_text_id', None) is None:
            self.hp_text_id = self.canvas.create_text(10, 10, anchor="nw", text=f"HP: {self.player.hp}", fill="white", font="Times 16 bold", tags="HUD")
        else:
            self.canvas.itemconfig(self.hp_text_id, text=f"HP: {self.player.hp}")
        if getattr(self, 'score_text_id', None) is None:
            self.score_text_id = self.canvas.create_text(10, 34, anchor="nw", text=f"Score: {self.score}", fill="white", font="Times 16 bold", tags="HUD")
        else:
            self.canvas.itemconfig(self.score_text_id, text=f"Score: {self.score}")
        self.request_scene = None
        self.player.image_id = None
        if getattr(self, 'weapon_image_id', None) is not None:
            try:
                self.canvas.delete(self.weapon_image_id)
            except Exception:
                pass
        self.weapon_image_id = None
        self.weapon_photo = None
        self.weapon_angle = 0.0
        self.weapon_active = True

    def clear_entities(self):
        try:
            if getattr(self.player, 'image_id', None) is not None:
                self.canvas.delete(self.player.image_id)
                self.player.image_id = None
        except Exception:
            pass
        for e in list(self.enemies):
            try:
                if getattr(e, 'image_id', None) is not None:
                    self.canvas.delete(e.image_id)
                    e.image_id = None
            except Exception:
                pass
        try:
            if getattr(self, 'hp_text_id', None) is not None:
                self.canvas.delete(self.hp_text_id)
                self.hp_text_id = None
        except Exception:
            pass
        try:
            if getattr(self, 'score_text_id', None) is not None:
                self.canvas.delete(self.score_text_id)
                self.score_text_id = None
        except Exception:
            pass
        try:
            if getattr(self, 'weapon_image_id', None) is not None:
                self.canvas.delete(self.weapon_image_id)
                self.weapon_image_id = None
                self.weapon_photo = None
        except Exception:
            pass

    def display(self):
        self.player.update(self.keys, self.world_w, self.world_h)

        desired_cam_x = self.player.world_x - self.screen_center_x
        desired_cam_y = self.player.world_y - self.screen_center_y
        self.camera_x = max(0, min(desired_cam_x, self.world_w - self.screen_w))
        self.camera_y = max(0, min(desired_cam_y, self.world_h - self.screen_h))

        p_img = self.player.images_r[0]
        p_w = p_img.width()
        p_h = p_img.height()
        px, py = self.player.get_world_pos()

        for e in list(self.enemies):
            e.speed = min(self.enemy_max_speed, self.enemy_base_speed + self.score * self.enemy_speed_per_score)
            e.update((px, py), self.world_w, self.world_h)
            ew = e.sprite.width() if (e.sprite is not None) else 32
            eh = e.sprite.height() if (e.sprite is not None) else 32
            ex, ey = e.world_x, e.world_y

            # 충돌 범위에 마진 적용 (플레이어와 적)
            overlapping = (abs(px - ex) * 2 < (p_w + ew + self.enemy_hit_margin)) and (abs(py - ey) * 2 < (p_h + eh + self.enemy_hit_margin))
            if overlapping:
                if 32 in self.keys or 13 in self.keys:
                    # 플레이어 근접 공격: 데미지 적용
                    rx, ry = e.world_x, e.world_y
                    alive = e.take_damage(1)
                    if not alive:
                        try:
                            if getattr(e, 'image_id', None) is not None:
                                self.canvas.delete(e.image_id)
                        except Exception:
                            pass
                        if e in self.enemies:
                            self.enemies.remove(e)
                        # 즉시 보충 및 리스폰 스케줄
                        if len(self.enemies) < self.MAX_ENEMIES:
                            self._spawn_enemy_random()
                        self._schedule_enemy_respawn(rx, ry)
                        self.score += 1
                        sx = px - self.camera_x
                        sy = py - self.camera_y - 40
                        txt = self.canvas.create_text(sx, sy, text="+1", fill="yellow", font="Times 14 bold")
                        self.canvas.after(600, lambda id=txt: self.canvas.delete(id))
                        self.canvas.itemconfig(self.score_text_id, text=f"Score: {self.score}")
                    else:
                        # 히트 이펙트(원하면 추가)
                        pass
                    continue
                else:
                    e.contact_timer += 1
                    if e.contact_timer >= e.attack_cooldown:
                        e.contact_timer = 0
                        self.player.take_damage(10)
                        sx = px - self.camera_x
                        sy = py - self.camera_y - 40
                        txt = self.canvas.create_text(sx, sy, text="-10", fill="red", font="Times 14 bold")
                        self.canvas.after(600, lambda id=txt: self.canvas.delete(id))
                        self.canvas.itemconfig(self.hp_text_id, text=f"HP: {self.player.hp}")
                        if self.player.hp <= 0:
                            self.request_scene = {'target': 4, 'score': self.score}
                            return

        self.canvas.coords(self.bg_id, -self.camera_x, -self.camera_y)
        self.player.draw(self.canvas, self.camera_x, self.camera_y)

        if self.weapon_orig is not None and self.weapon_active:
            self.weapon_angle = (self.weapon_angle + self.weapon_speed) % 360
            rotated = self.weapon_orig.rotate(-self.weapon_angle, resample=Image.BICUBIC, expand=True)
            rot_w, rot_h = rotated.size
            self.weapon_photo = ImageTk.PhotoImage(rotated)
            player_screen_x = self.player.world_x - self.camera_x
            player_screen_y = self.player.world_y - self.camera_y
            rad = math.radians(self.weapon_angle)
            wx = player_screen_x + self.weapon_radius * math.cos(rad)
            wy = player_screen_y + self.weapon_radius * math.sin(rad)

            if self.weapon_image_id is None:
                self.weapon_image_id = self.canvas.create_image(wx, wy, image=self.weapon_photo, tags="Weapon")
            else:
                self.canvas.coords(self.weapon_image_id, wx, wy)
                self.canvas.itemconfig(self.weapon_image_id, image=self.weapon_photo)

            hits = []
            for e in list(self.enemies):
                ew = e.sprite.width() if (e.sprite is not None) else e.sprite.width() * e.sprite.zoom
                eh = e.sprite.height() if (e.sprite is not None) else e.sprite.height() * e.sprite.zoom
                ex_s = e.world_x - self.camera_x
                ey_s = e.world_y - self.camera_y
                if (abs(wx - ex_s) * 2 < (rot_w + ew + self.weapon_hit_margin)) and (abs(wy - ey_s) * 2 < (rot_h + eh + self.weapon_hit_margin)):
                    hits.append((e, ex_s, ey_s))

            if hits:
                e, ex_s, ey_s = hits[0]
                rx, ry = e.world_x, e.world_y
                alive = e.take_damage(1)
                if not alive:
                    try:
                        if getattr(e, 'image_id', None) is not None:
                            self.canvas.delete(e.image_id)
                    except Exception:
                        pass
                    if e in self.enemies:
                        self.enemies.remove(e)
                    if len(self.enemies) < self.MAX_ENEMIES:
                        self._spawn_enemy_random()
                    self._schedule_enemy_respawn(rx, ry)
                    sx = wx
                    sy = wy
                    self.score += 1
                    hit_txt = self.canvas.create_text(sx, sy, text="+1", fill="yellow", font="Times 12 bold")
                    self.canvas.after(600, lambda id=hit_txt: self.canvas.delete(id))
                    self.canvas.itemconfig(self.score_text_id, text=f"Score: {self.score}")
                else:
                    # 히트 이펙트(원하면 추가)
                    pass

        for e in list(self.enemies):
            e.draw(self.canvas, self.camera_x, self.camera_y)

        if getattr(self, 'hp_text_id', None) is not None:
            self.canvas.itemconfig(self.hp_text_id, text=f"HP: {self.player.hp}")
        if getattr(self, 'score_text_id', None) is not None:
            self.canvas.itemconfig(self.score_text_id, text=f"Score: {self.score}")

    def pack(self):
        self.canvas.pack(expand=True, fill=BOTH)

    def unpack(self):
        self.canvas.pack_forget()

    def keyPresseHandler(self, event):
        self.keys.add(event.keycode)

    def keyPresseReleaseHandler(self, event):
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)
        if (hasattr(event, 'keysym') and event.keysym == 'Escape') or event.keycode == 27:
            return 0
        return -1

    def destroy(self):
        self.clear_entities()
        try:
            self.canvas.delete(self.bg_id)
        except Exception:
            pass
        self.canvas.destroy()    


class PauseCanvas:
    def __init__(self, window):
        self.window = window
        self.canvas = Canvas(self.window, bg="black")
        self.keys = set()

        self.canvas.create_text(640, 300, text="일시정지", fill="white", font="Times 30 bold")
        self.canvas.create_text(640, 380, text="계속하기", fill="white", font="Times 20")
        self.canvas.create_text(640, 430, text="메뉴로 돌아가기", fill="white", font="Times 20")

        arrow_path = os.path.join(os.path.dirname(__file__), "image", "select_arrow.png")
        self.select_arrow = PhotoImage(file=arrow_path).subsample(20)

        self.selectImage = self.canvas.create_image(685, 400, image=self.select_arrow, tags="select")

        self.pause_index = 0  # 0 = 계속하기 / 1 = 메뉴로 돌아가기

    def display(self):
        pass

    def pack(self):
        self.canvas.pack(expand=True, fill=BOTH)

    def unpack(self):
        self.canvas.pack_forget()

    def keyPresseHandler(self, event):
        self.keys.add(event.keycode)

    def keyPresseReleaseHandler(self, event):

        if event.keycode in self.keys:
            self.keys.remove(event.keycode)

        if (event.keycode == 38 or event.keycode == 87) and self.pause_index > 0:
            self.pause_index -= 1

            self.canvas.move(self.selectImage, 0, -50)
            return -1

        if (event.keycode == 40 or event.keycode == 83) and self.pause_index < 1:
            self.pause_index += 1
            self.canvas.move(self.selectImage, 0, 50)
            return -1

        if event.keycode == 13 or event.keycode == 32:
            if self.pause_index == 0:
                return 2   # 계속하기
            elif self.pause_index == 1:
                return 0   # 메뉴로 돌아가기

        if event.keycode == 27:
            return 2

        return -1


class GameOverCanvas:
    def __init__(self, window):
        self.window = window
        self.canvas = Canvas(self.window, bg="black")
        self.keys = set()

        self.canvas.create_text(640, 220, text="Game Over", fill="red", font="Times 40 bold")
        self.score_text = self.canvas.create_text(640, 280, text="Score: 0", fill="white", font="Times 20 bold")
        self.canvas.create_text(640, 360, text="다시 시작", fill="white", font="Times 20")
        self.canvas.create_text(640, 410, text="메뉴로 돌아가기", fill="white", font="Times 20")

        arrow_path = os.path.join(os.path.dirname(__file__), "image", "select_arrow.png")
        self.select_arrow = PhotoImage(file=arrow_path).subsample(20)
        self.selectImage = self.canvas.create_image(665, 360, image=self.select_arrow, tags="select")

        self.go_index = 0  # 0 = restart / 1 = menu

    def set_score(self, score):
        self.canvas.itemconfig(self.score_text, text=f"Score: {score}")

    def display(self):
        pass

    def pack(self):
        self.canvas.pack(expand=True, fill=BOTH)
        try:
            self.canvas.focus_set()
        except Exception:
            pass

    def unpack(self):
        self.canvas.pack_forget()

    def keyPresseHandler(self, event):
        self.keys.add(event.keycode)

    def keyPresseReleaseHandler(self, event):
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)

        if (event.keycode == 38 or event.keycode == 87) and self.go_index > 0:
            self.go_index -= 1
            self.canvas.move(self.selectImage, 0, -50)
            return -1

        if (event.keycode == 40 or event.keycode == 83) and self.go_index < 1:
            self.go_index += 1
            self.canvas.move(self.selectImage, 0, 50)
            return -1

        if event.keycode == 13 or event.keycode == 32:
            if self.go_index == 0:
                return 2  # restart stage
            else:
                return 0  # menu

        if event.keycode == 27:
            return 0

        return -1


class MainCanvas:
    def __init__(self):
        # 기본 윈도우 tk 열기
        self.window = Tk()
        self.window.title("farmingSurvival")
        self.window.geometry("1280x960")

        # 음악 관련 상태 초기화
        self.music_playing = False
        self.music_error = None

        # pygame mixer 초기화 및 BGM 재생 시도
        try:
            pygame.mixer.init()
            music_path = os.path.join(os.path.dirname(__file__), "sound", "Jim Yosef - Firefly [NCS Release].mp3")
            if os.path.exists(music_path):
                try:
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)  # 무한루프
                    self.music_playing = True
                    print("[BGM] Playing:", music_path)
                except Exception as ex:
                    self.music_playing = False
                    self.music_error = f"pygame.mixer.music.load/play error: {ex}"
                    print("[BGM] load/play error:", ex)
            else:
                self.music_playing = False
                self.music_error = f"file not found: {music_path}"
                print("[BGM] file not found:", music_path)
        except Exception as ex:
            self.music_playing = False
            self.music_error = f"mixer init error: {ex}"
            print("[BGM] mixer init error:", ex)

        # 다중캔버스
        self.menu = MenuCanvas(self.window)
        self.menu.pack()
        self.setting = settingCanvas(self.window)
        self.stage = StageCanvas(self.window)
        self.pause = PauseCanvas(self.window)
        self.gameover = GameOverCanvas(self.window)

        self.canvas_list = []
        self.canvas_list.append(self.menu)     # 0
        self.canvas_list.append(self.setting)  # 1
        self.canvas_list.append(self.stage)    # 2
        self.canvas_list.append(self.pause)    # 3
        self.canvas_list.append(self.gameover) # 4

        self.scene_index = 0 # 0 = 메뉴 / 1 = 설정 / 2 = 스테이지 / 3 = 일시정지 / 4 = 게임오버

        # BGM 볼륨 초기 동기화
        try:
            self.prev_bgm_index = getattr(self.setting, 'bgm_balance_index', 5)
        except Exception:
            self.prev_bgm_index = 5
        if self.music_playing:
            try:
                pygame.mixer.music.set_volume(max(0.0, min(1.0, self.prev_bgm_index / 10.0)))
            except Exception:
                pass

        # 키보드 바인딩
        self.keys = set()
        self.window.bind("<KeyPress>", self.keyPresseHandler)
        self.window.bind("<KeyRelease>", self.keyPresseReleaseHandler)
        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

        while 1:
            try:
                # setting에서 BGM 인덱스 변경시 실시간 반영
                try:
                    current_bgm_index = getattr(self.setting, 'bgm_balance_index', self.prev_bgm_index)
                    if current_bgm_index != self.prev_bgm_index and self.music_playing:
                        vol = max(0.0, min(1.0, current_bgm_index / 10.0))
                        try:
                            pygame.mixer.music.set_volume(vol)
                        except Exception:
                            pass
                        self.prev_bgm_index = current_bgm_index
                except Exception:
                    pass

                # 현재 씬 업데이트
                current = self.canvas_list[self.scene_index]
                current.display()

                # per-frame 
                if hasattr(current, 'request_scene') and current.request_scene:
                    req = current.request_scene
                    current.request_scene = None
                    # 게임오버 요청
                    if req.get('target') == 4:
                        try:
                            self.stage.clear_entities()
                        except Exception:
                            pass
                        self.stage.unpack()
                        self.scene_index = 4
                        self.gameover.set_score(req.get('score', 0))
                        self.gameover.pack()

            except TclError:
                break

            self.window.after(33)
            self.window.update()

        # 루프 종료 시 믹서 정리
        try:
            if self.music_playing:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
        except Exception:
            pass

    def keyPresseHandler(self, event):
        self.canvas_list[self.scene_index].keyPresseHandler(event)

    def keyPresseReleaseHandler(self, event):
        result = self.canvas_list[self.scene_index].keyPresseReleaseHandler(event)
        prev_scene = self.scene_index

        # setting <=> menu
        if prev_scene == 1 and result == 0:
            self.setting.unpack()
            self.scene_index = 0
            self.menu.pack()
        elif prev_scene == 0 and result == 1:
            self.menu.unpack()
            self.scene_index = 1
            self.setting.pack()

        # menu -> stage
        elif prev_scene == 0 and result == 2:
            # 난이도 설정을 Stage에 반영
            try:
                self.stage.set_difficulty(getattr(self.setting, 'stage_level_index', 0))
            except Exception:
                pass
            self.menu.unpack()
            self.scene_index = 2
            self.stage.pack()

        # stage -> pause
        elif prev_scene == 2 and result == 0:
            self.stage.unpack()
            self.scene_index = 3
            self.pause.pack()

        # pause -> menu
        elif prev_scene == 3 and result == 0:
            self.pause.unpack()
            self.scene_index = 0
            self.menu.pack()

        # pause -> stage (계속하기)
        elif prev_scene == 3 and result == 2:
            self.pause.unpack()
            self.scene_index = 2
            self.stage.pack()

        # gameover -> menu: Stage 초기화 
        elif prev_scene == 4 and result == 0:
            self.gameover.unpack()
            try:
                self.stage.reset()
            except Exception:
                pass
            self.scene_index = 0
            self.menu.pack()

        # gameover -> Stage 초기화 (restart)
        elif prev_scene == 4 and result == 2:
            self.gameover.unpack()
            try:
                # 난이도 설정을 Stage에 반영(설정값 변경 후 재시작 반영)
                self.stage.set_difficulty(getattr(self.setting, 'stage_level_index', 0))
                self.stage.reset()
            except Exception:
                pass
            self.scene_index = 2
            self.stage.pack()

    def onClose(self):
        try:
            if getattr(self, 'music_playing', False):
                pygame.mixer.music.stop()
                pygame.mixer.quit()
        except Exception:
            pass
        self.window.destroy()

if __name__ == "__main__":
    MainCanvas()
