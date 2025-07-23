import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 60
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - 100) // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
YELLOW = (255, 255, 100)
PURPLE = (200, 100, 255)
GRAY = (200, 200, 200)

class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0  # 0=right, 1=down, 2=left, 3=up
        
    def move_forward(self):
        if self.direction == 0:  # right
            self.x = min(self.x + 1, GRID_WIDTH - 1)
        elif self.direction == 1:  # down
            self.y = min(self.y + 1, GRID_HEIGHT - 1)
        elif self.direction == 2:  # left
            self.x = max(self.x - 1, 0)
        elif self.direction == 3:  # up
            self.y = max(self.y - 1, 0)
    
    def turn_right(self):
        self.direction = (self.direction + 1) % 4
    
    def turn_left(self):
        self.direction = (self.direction - 1) % 4

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Robot Programming Game for Kids!")
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.robot = Robot(0, 0)
        self.treasures = set()
        self.score = 0
        self.commands = []
        self.executing = False
        self.command_index = 0
        self.execution_timer = 0
        
        self.generate_treasures()
    
    def generate_treasures(self):
        """Generate random treasure positions"""
        self.treasures.clear()
        for _ in range(5):
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                if (x, y) not in self.treasures and (x, y) != (self.robot.x, self.robot.y):
                    self.treasures.add((x, y))
                    break
    
    def draw_grid(self):
        """Draw the game grid"""
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT - 100))
        for y in range(0, SCREEN_HEIGHT - 100, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y))
    
    def draw_robot(self):
        """Draw the robot with direction indicator"""
        x = self.robot.x * GRID_SIZE + GRID_SIZE // 2
        y = self.robot.y * GRID_SIZE + GRID_SIZE // 2
        
        # Draw robot body
        pygame.draw.circle(self.screen, BLUE, (x, y), GRID_SIZE // 3)
        
        # Draw direction indicator
        if self.robot.direction == 0:  # right
            pygame.draw.polygon(self.screen, RED, [(x + 15, y), (x + 25, y - 8), (x + 25, y + 8)])
        elif self.robot.direction == 1:  # down
            pygame.draw.polygon(self.screen, RED, [(x, y + 15), (x - 8, y + 25), (x + 8, y + 25)])
        elif self.robot.direction == 2:  # left
            pygame.draw.polygon(self.screen, RED, [(x - 15, y), (x - 25, y - 8), (x - 25, y + 8)])
        elif self.robot.direction == 3:  # up
            pygame.draw.polygon(self.screen, RED, [(x, y - 15), (x - 8, y - 25), (x + 8, y - 25)])
    
    def draw_treasures(self):
        """Draw treasure gems"""
        for tx, ty in self.treasures:
            x = tx * GRID_SIZE + GRID_SIZE // 2
            y = ty * GRID_SIZE + GRID_SIZE // 2
            # Draw a diamond shape
            pygame.draw.polygon(self.screen, YELLOW, [
                (x, y - 15), (x + 12, y - 3), (x, y + 15), (x - 12, y - 3)
            ])
            pygame.draw.polygon(self.screen, (255, 215, 0), [
                (x, y - 10), (x + 8, y), (x, y + 10), (x - 8, y)
            ])
    
    def draw_ui(self):
        """Draw the user interface"""
        # Draw control panel background
        pygame.draw.rect(self.screen, (240, 240, 240), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
        pygame.draw.line(self.screen, BLACK, (0, SCREEN_HEIGHT - 100), (SCREEN_WIDTH, SCREEN_HEIGHT - 100), 2)
        
        # Draw score
        score_text = self.font_big.render(f"Treasures Found: {self.score}/5", True, BLACK)
        self.screen.blit(score_text, (10, SCREEN_HEIGHT - 90))
        
        # Draw instructions
        if not self.executing:
            inst1 = self.font_small.render("Commands: SPACE=Move Forward, LEFT=Turn Left, RIGHT=Turn Right", True, BLACK)
            inst2 = self.font_small.render("Press ENTER to run your program! Press R to reset.", True, BLACK)
            self.screen.blit(inst1, (10, SCREEN_HEIGHT - 60))
            self.screen.blit(inst2, (10, SCREEN_HEIGHT - 35))
        else:
            exec_text = self.font_small.render(f"Executing command {self.command_index + 1} of {len(self.commands)}", True, BLACK)
            self.screen.blit(exec_text, (10, SCREEN_HEIGHT - 60))
        
        # Draw current commands
        if self.commands:
            cmd_text = "Program: " + " → ".join(self.commands[-10:])  # Show last 10 commands
            if len(self.commands) > 10:
                cmd_text = "... → " + cmd_text[9:]
            command_surface = self.font_small.render(cmd_text, True, PURPLE)
            self.screen.blit(command_surface, (300, SCREEN_HEIGHT - 90))
    
    def check_treasure_collection(self):
        """Check if robot collected a treasure"""
        if (self.robot.x, self.robot.y) in self.treasures:
            self.treasures.remove((self.robot.x, self.robot.y))
            self.score += 1
            if self.score == 5:
                self.show_victory()
    
    def show_victory(self):
        """Show victory message"""
        victory_text = self.font_big.render("🎉 YOU WON! Great Programming! 🎉", True, GREEN)
        text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.draw.rect(self.screen, WHITE, text_rect.inflate(20, 10))
        pygame.draw.rect(self.screen, GREEN, text_rect.inflate(20, 10), 3)
        self.screen.blit(victory_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.robot = Robot(0, 0)
        self.score = 0
        self.commands = []
        self.executing = False
        self.command_index = 0
        self.generate_treasures()
    
    def execute_commands(self):
        """Execute the programmed commands"""
        if not self.executing or not self.commands:
            return
        
        self.execution_timer += self.clock.get_time()
        if self.execution_timer >= 800:  # Execute command every 800ms
            if self.command_index < len(self.commands):
                command = self.commands[self.command_index]
                
                if command == "FORWARD":
                    self.robot.move_forward()
                elif command == "LEFT":
                    self.robot.turn_left()
                elif command == "RIGHT":
                    self.robot.turn_right()
                
                self.check_treasure_collection()
                self.command_index += 1
                self.execution_timer = 0
            else:
                self.executing = False
                self.command_index = 0
    
    def handle_input(self, event):
        """Handle keyboard input"""
        if event.type == pygame.KEYDOWN and not self.executing:
            if event.key == pygame.K_SPACE:
                self.commands.append("FORWARD")
            elif event.key == pygame.K_LEFT:
                self.commands.append("LEFT")
            elif event.key == pygame.K_RIGHT:
                self.commands.append("RIGHT")
            elif event.key == pygame.K_RETURN and self.commands:
                self.executing = True
                self.command_index = 0
                self.execution_timer = 0
            elif event.key == pygame.K_r:
                self.reset_game()
            elif event.key == pygame.K_BACKSPACE and self.commands:
                self.commands.pop()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_input(event)
            
            # Execute commands if running
            self.execute_commands()
            
            # Draw everything
            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_treasures()
            self.draw_robot()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    print("🤖 Welcome to Robot Programming Game! 🤖")
    print("Help your robot collect all the treasures!")
    print("Use SPACE (move forward), LEFT arrow (turn left), RIGHT arrow (turn right)")
    print("Press ENTER to run your program, R to reset, BACKSPACE to undo last command")
    print("Have fun learning to code!")
    
    game = Game()
    game.run()
