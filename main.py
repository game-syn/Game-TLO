#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List

import pygame

SAVE_PATH = Path.home() / ".the_last_order_save.json"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
HUD_HEIGHT = 90

MISSION_DATA = [
    {
        "name": "Operation White Dusk",
        "brief": "Break through the convoy route and secure the extraction corridor.",
        "map": [
            "############################",
            "#.............#............#",
            "#..######.....#..####....##",
            "#..#....#.....#.....#.....#",
            "#..#....#.....#.....#.....#",
            "#..#....#..#..#..#..#.....#",
            "#..#....#..#..#..#..#.....#",
            "#......#.................#",
            "#.####.#.######.#######..##",
            "#..............#........##",
            "############################",
        ],
        "players": [(2.5, 2.5), (8.5, 8.5)],
        "enemies": [(4.5, 3.5), (7.5, 5.5), (10.5, 4.5)],
    },
    {
        "name": "Blackwater Lift",
        "brief": "Hold the extraction lift and neutralise the blockade team.",
        "map": [
            "############################",
            "#..............#...........#",
            "#..#####.......#....###....#",
            "#..#...#.......#....#......#",
            "#..#...#.......#....#......#",
            "#..#...#...................#",
            "#..#...#...#######...###...#",
            "#..#...#...#.....#...#.....#",
            "#..#...#...#..#..#...#.....#",
            "#.................#........#",
            "############################",
        ],
        "players": [(2.5, 2.5), (9.5, 8.5)],
        "enemies": [(4.2, 3.8), (5.8, 7.0), (8.5, 3.0), (10.0, 7.2)],
    },
    {
        "name": "Glass Harbor",
        "brief": "Sweep the harbor warehouses and prevent a data breach.",
        "map": [
            "############################",
            "#.................#.......#",
            "#..####..####....#...#...##",
            "#..#..#..#..#....#...#....#",
            "#..#..#..#..#....#...#....#",
            "#..#..#..#..#....#...#....#",
            "#..#..#..#..#....#...#....#",
            "#..#..#..#..#....#...#....#",
            "#..#........#....#...#....#",
            "#..######.##....#...#....##",
            "############################",
        ],
        "players": [(2.5, 7.0), (8.5, 2.0)],
        "enemies": [(4.5, 6.0), (6.5, 6.5), (9.0, 5.5), (10.0, 8.0)],
    },
    {
        "name": "Zero Hour",
        "brief": "Intercept the command channel and keep their forward squad under siege.",
        "map": [
            "############################",
            "#.............#...........##",
            "#..####.......#.....####..#",
            "#..#..#.......#.....#..#..#",
            "#..#..#................#..#",
            "#..#..#...####....####...#.#",
            "#..#..#...#..#....#..#...#.#",
            "#..#..#...#..#....#..#...#.#",
            "#..#..#...#..#....#..#...#.#",
            "#...........##.............#",
            "############################",
        ],
        "players": [(2.5, 2.8), (8.5, 7.5)],
        "enemies": [(4.3, 3.5), (5.8, 5.5), (8.5, 4.5), (9.8, 7.0), (6.8, 8.0)],
    },
    {
        "name": "Shatterline",
        "brief": "Traverse the frozen corridor and break the hostile signal net.",
        "map": [
            "############################",
            "#...............#..........#",
            "#..####....####.#.####.....#",
            "#..#..#....#..#.#.#..#.....#",
            "#..#..#....#..#.#.#..#.....#",
            "#..#..#....#..#.#.#..#.....#",
            "#..#..#....#..#.#.#..#.....#",
            "#..#..#....#..#.#.#..#.....#",
            "#..#..#....#..#.#.#..#.....#",
            "#..............#...........#",
            "############################",
        ],
        "players": [(2.0, 2.2), (9.0, 7.5)],
        "enemies": [(3.8, 2.5), (6.2, 3.5), (9.0, 5.5), (7.8, 8.0), (4.0, 7.0)],
    },
    {
        "name": "Final Orders",
        "brief": "Secure the command hub and end the betrayal before the strike reaches the capital.",
        "map": [
            "############################",
            "#...........#..............#",
            "#.######....#..######......#",
            "#....#......#......#.......#",
            "#....#......#......#.......#",
            "#....#......#......#.......#",
            "#....#######.#######........#",
            "#......................#...#",
            "#..####...###...####....#...#",
            "#........#...#...........#.#",
            "############################",
        ],
        "players": [(2.4, 2.3), (9.5, 6.6)],
        "enemies": [(4.5, 2.4), (6.0, 4.0), (8.2, 6.0), (10.0, 3.5), (7.2, 8.1), (4.5, 7.5)],
    },
]


@dataclass
class Player:
    name: str
    x: float
    y: float
    angle: float = 0.0
    health: int = 100
    ammo: int = 20
    alive: bool = True
    sprint: float = 1.0

    @property
    def pos(self):
        return (self.x, self.y)


@dataclass
class Enemy:
    x: float
    y: float
    hp: int = 40
    alive: bool = True


@dataclass
class Projectile:
    x: float
    y: float
    angle: float
    owner: str
    ttl: float = 1.20


@dataclass
class MissionState:
    name: str
    brief: str
    map_data: List[str]
    player_spawn: List[tuple]
    enemy_positions: List[tuple]
    title: str = ""


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 22)
        self.big_font = pygame.font.SysFont(None, 42)
        self.running = True
        self.state = "menu"
        self.saved_mission = self.load_save()
        self.current_mission_index = self.saved_mission.get("mission_index", 0)
        self.level_start_text = "Mission briefing"
        self.start_new_mission(self.current_mission_index)

    def start_new_mission(self, mission_index: int):
        self.current_mission_index = max(0, min(mission_index, len(MISSION_DATA) - 1))
        mission = MISSION_DATA[self.current_mission_index]
        self.mission = MissionState(
            name=mission["name"],
            brief=mission["brief"],
            map_data=mission["map"],
            player_spawn=mission["players"],
            enemy_positions=mission["enemies"],
            title=mission["name"],
        )
        self.players = [
            Player("Player 1", self.mission.player_spawn[0][0], self.mission.player_spawn[0][1], 0.0),
            Player("Player 2", self.mission.player_spawn[1][0], self.mission.player_spawn[1][1], math.pi),
        ]
        self.enemies = [
            Enemy(x, y) for x, y in self.mission.enemy_positions
        ]
        self.projectiles: List[Projectile] = []
        self.mission_complete = False
        self.state = "menu"
        self.level_start_text = f"{self.mission.name}: {self.mission.brief}"
        self.save_game()

    def load_save(self):
        if not SAVE_PATH.exists():
            return {"mission_index": 0}
        try:
            with SAVE_PATH.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
                return data if isinstance(data, dict) else {"mission_index": 0}
        except (OSError, ValueError):
            return {"mission_index": 0}

    def save_game(self):
        payload = {"mission_index": self.current_mission_index}
        with SAVE_PATH.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle)

    def is_wall(self, x: float, y: float) -> bool:
        if x < 0 or y < 0:
            return True
        map_w = len(self.mission.map_data[0])
        map_h = len(self.mission.map_data)
        if x >= map_w or y >= map_h:
            return True
        cell_x = int(x)
        cell_y = int(y)
        try:
            return self.mission.map_data[cell_y][cell_x] == '#'
        except IndexError:
            return True

    def player_move(self, player: Player, move_x: float, move_y: float, dt: float):
        new_x = player.x + move_x * dt * 2.5 * player.sprint
        new_y = player.y + move_y * dt * 2.5 * player.sprint
        if not self.is_wall(new_x, player.y):
            player.x = new_x
        if not self.is_wall(player.x, new_y):
            player.y = new_y

    def cast_ray(self, x, y, angle, max_depth=12.0, steps=200):
        for _ in range(steps):
            step = _ / steps * max_depth
            px = x + math.cos(angle) * step
            py = y + math.sin(angle) * step
            if self.is_wall(px, py):
                return step
        return max_depth

    def render_scene(self, viewport_rect, player: Player):
        width = viewport_rect.width
        height = viewport_rect.height

        sky = (14, 18, 26)
        floor = (26, 30, 35)
        wall_base = (88, 100, 110)

        surface = pygame.Surface((width, height))
        surface.fill(sky)
        for y in range(height):
            shade = 1.0 - (y / height)
            color = tuple(max(0, min(255, int(c * shade))) for c in floor)
            pygame.draw.line(surface, color, (0, y), (width, y))

        # draw walls and enemies in a first-person perspective
        for x in range(width):
            ray_angle = player.angle - 0.7 + (x / width) * 1.4
            dist = self.cast_ray(player.x, player.y, ray_angle)
            if dist <= 0:
                continue
            wall_height = min(height * 0.85, (height / max(dist, 0.2)) * 0.9)
            start_y = (height - wall_height) / 2
            shade = max(0.15, 1.0 - dist / 10.0)
            color = tuple(max(0, min(255, int(c * shade))) for c in wall_base)
            rect = pygame.Rect(x, int(start_y), 2, int(wall_height))
            pygame.draw.rect(surface, color, rect)

        # sprites
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            rel_x = enemy.x - player.x
            rel_y = enemy.y - player.y
            dist = math.hypot(rel_x, rel_y)
            if dist <= 0.1:
                continue
            angle = math.atan2(rel_y, rel_x) - player.angle
            while angle < -math.pi:
                angle += 2 * math.pi
            while angle > math.pi:
                angle -= 2 * math.pi
            if abs(angle) > 0.9:
                continue
            sprite_screen_x = (angle + 0.7) / 1.4 * width
            sprite_height = min(height * 0.7, (height / max(dist, 0.2)) * 0.65)
            sprite_width = sprite_height * 0.6
            sprite_rect = pygame.Rect(
                int(sprite_screen_x - sprite_width / 2),
                int((height - sprite_height) / 2),
                int(sprite_width),
                int(sprite_height),
            )
            pygame.draw.rect(surface, (180, 30, 30), sprite_rect)

        self.screen.blit(surface, viewport_rect.topleft)

    def draw_hud(self, player_index):
        player = self.players[player_index]
        panel = pygame.Rect(0, 0, WINDOW_WIDTH // 2, HUD_HEIGHT)
        if player_index == 1:
            panel.x = WINDOW_WIDTH // 2
        health = max(0, player.health)
        ammo = max(0, player.ammo)
        text = self.font.render(f"{player.name}  HP {health}  AMMO {ammo}", True, (255, 255, 255))
        self.screen.blit(text, (panel.x + 20, 15))
        text2 = self.font.render(f"Mission: {self.mission.name}", True, (255, 255, 255))
        self.screen.blit(text2, (panel.x + 20, 40))
        if player_index == 0:
            objective = self.font.render(self.mission.brief, True, (200, 220, 255))
            self.screen.blit(objective, (20, 60))

    def draw_menu(self):
        self.screen.fill((8, 12, 18))
        title = self.big_font.render("THE LAST ORDER", True, (210, 220, 230))
        subtitle = self.font.render("Local split-screen co-op prototype", True, (180, 190, 210))
        self.screen.blit(title, (WINDOW_WIDTH / 2 - title.get_width() / 2, 180))
        self.screen.blit(subtitle, (WINDOW_WIDTH / 2 - subtitle.get_width() / 2, 240))
        mission_text = self.font.render(f"Mission {self.current_mission_index + 1}: {self.mission.name}", True, (220, 230, 240))
        self.screen.blit(mission_text, (WINDOW_WIDTH / 2 - mission_text.get_width() / 2, 300))
        detail = self.font.render(self.mission.brief, True, (200, 200, 200))
        self.screen.blit(detail, (WINDOW_WIDTH / 2 - detail.get_width() / 2, 340))
        hint = self.font.render("Press ENTER to deploy and continue.  Q/E = turn, WASD = move, Space = fire.", True, (160, 220, 180))
        self.screen.blit(hint, (WINDOW_WIDTH / 2 - hint.get_width() / 2, 420))
        p2 = self.font.render("P2: IJKL move, U/O turn, Right Ctrl fire", True, (160, 220, 180))
        self.screen.blit(p2, (WINDOW_WIDTH / 2 - p2.get_width() / 2, 450))

    def draw_end_screen(self):
        self.screen.fill((8, 10, 14))
        title = self.big_font.render("MISSION COMPLETE", True, (160, 230, 180))
        self.screen.blit(title, (WINDOW_WIDTH / 2 - title.get_width() / 2, 180))
        sub = self.font.render(f"{self.mission.name} secured.", True, (212, 220, 220))
        self.screen.blit(sub, (WINDOW_WIDTH / 2 - sub.get_width() / 2, 250))
        hint = self.font.render("Press ENTER to continue to the next mission or R to restart.", True, (220, 220, 220))
        self.screen.blit(hint, (WINDOW_WIDTH / 2 - hint.get_width() / 2, 330))

    def handle_combat(self, dt: float):
        for projectile in list(self.projectiles):
            projectile.x += math.cos(projectile.angle) * 0.18
            projectile.y += math.sin(projectile.angle) * 0.18
            projectile.ttl -= dt
            if projectile.ttl <= 0 or self.is_wall(projectile.x, projectile.y):
                self.projectiles.remove(projectile)
                continue
            for enemy in self.enemies:
                if not enemy.alive:
                    continue
                if math.hypot(projectile.x - enemy.x, projectile.y - enemy.y) < 0.45:
                    enemy.hp -= 25
                    self.projectiles.remove(projectile)
                    if enemy.hp <= 0:
                        enemy.alive = False
                    break

    def fire_from_player(self, player_name: str, angle: float):
        if player_name == "Player 1":
            player = self.players[0]
        else:
            player = self.players[1]
        if player.ammo <= 0:
            return
        player.ammo -= 1
        self.projectiles.append(Projectile(player.x + math.cos(angle) * 0.4, player.y + math.sin(angle) * 0.4, angle, player_name))

    def update(self, dt: float):
        if self.state == "menu":
            return
        if self.state == "game":
            p1, p2 = self.players
            # Player 1 controls: WASD + Q/E
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player_move(p1, math.cos(p1.angle), math.sin(p1.angle), dt)
            if keys[pygame.K_s]:
                self.player_move(p1, -math.cos(p1.angle), -math.sin(p1.angle), dt)
            if keys[pygame.K_a]:
                self.player_move(p1, -math.sin(p1.angle), math.cos(p1.angle), dt)
            if keys[pygame.K_d]:
                self.player_move(p1, math.sin(p1.angle), -math.cos(p1.angle), dt)
            if keys[pygame.K_q]:
                p1.angle -= dt * 1.8
            if keys[pygame.K_e]:
                p1.angle += dt * 1.8
            if keys[pygame.K_SPACE]:
                self.fire_from_player("Player 1", p1.angle)

            # Player 2 controls: IJKL + U/O
            if keys[pygame.K_i]:
                self.player_move(p2, math.cos(p2.angle), math.sin(p2.angle), dt)
            if keys[pygame.K_k]:
                self.player_move(p2, -math.cos(p2.angle), -math.sin(p2.angle), dt)
            if keys[pygame.K_j]:
                self.player_move(p2, -math.sin(p2.angle), math.cos(p2.angle), dt)
            if keys[pygame.K_l]:
                self.player_move(p2, math.sin(p2.angle), -math.cos(p2.angle), dt)
            if keys[pygame.K_u]:
                p2.angle -= dt * 1.8
            if keys[pygame.K_o]:
                p2.angle += dt * 1.8
            if keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]:
                self.fire_from_player("Player 2", p2.angle)

            self.handle_combat(dt)
            if not any(enemy.alive for enemy in self.enemies):
                self.mission_complete = True
                self.state = "mission_clear"
                if self.current_mission_index < len(MISSION_DATA) - 1:
                    self.current_mission_index += 1
                    self.save_game()
                else:
                    self.current_mission_index = len(MISSION_DATA) - 1
                    self.save_game()

    def render(self):
        if self.state in ("menu", "mission_clear"):
            self.screen.fill((16, 20, 28))
            if self.state == "menu":
                self.draw_menu()
            else:
                self.draw_end_screen()
            return

        self.screen.fill((14, 16, 20))
        split_rect = pygame.Rect(0, 0, WINDOW_WIDTH // 2, WINDOW_HEIGHT)
        self.render_scene(split_rect, self.players[0])
        split_rect.x = WINDOW_WIDTH // 2
        self.render_scene(split_rect, self.players[1])
        self.draw_hud(0)
        self.draw_hud(1)

        divider = pygame.Rect(WINDOW_WIDTH // 2 - 2, 0, 4, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, (220, 220, 220), divider)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_RETURN and self.state in ("menu", "mission_clear"):
                        if self.state == "menu":
                            self.state = "game"
                        else:
                            self.state = "game"
                            self.start_new_mission(self.current_mission_index)
                    if event.key == pygame.K_r and self.state == "mission_clear":
                        self.start_new_mission(self.current_mission_index)
            self.update(dt)
            self.render()
            pygame.display.flip()

        pygame.quit()


def main():
    pygame.init()
    pygame.display.set_caption("THE LAST ORDER")
    # Load a generated icon if present. The PNG is the most portable choice for pygame.
    asset_dir = Path(__file__).resolve().parent / "assets"
    for candidate in (asset_dir / "TheLastOrder.png", asset_dir / "TheLastOrder.ico"):
        if candidate.exists():
            try:
                pygame.display.set_icon(pygame.image.load(str(candidate)))
                break
            except pygame.error:
                continue
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    game = Game(screen)
    game.run()


if __name__ == "__main__":
    sys.exit(main())
