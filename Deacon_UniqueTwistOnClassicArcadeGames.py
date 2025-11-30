# Imports for system operations, GUI dialogs, and Pygame
import pygame
import tkinter as tk
from tkinter import ttk
from AppKit import NSAlert, NSApplication, NSApp, NSApplicationActivationPolicyRegular
from Cocoa import NSApplication, NSWindow, NSProgressIndicator, NSView, NSMakeRect, NSBackingStoreBuffered, NSWindowStyleMaskTitled, NSRunningApplication, NSApplicationActivateIgnoringOtherApps
import os
import math
import requests
import threading
import sys
from Foundation import NSObject

# Initialize pygame
pygame.init()

# Window dimensions and title
infoObject = pygame.display.Info()
WIDTH, HEIGHT = 1920, 1080
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED)
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Loop to ensure assets are loaded or downloaded
while True:
    pygame.init()
    try:
        # Try to load game assets
        pygame.display.set_icon(pygame.image.load('Assets/icon.png'))
        font = pygame.font.Font('Assets/flappy-font.ttf', 100)
        bg_image = pygame.image.load("Assets/background.png").convert()
        bg_height = bg_image.get_height()
        bg_width = bg_image.get_width()
        logo_image = pygame.transform.scale_by(pygame.image.load("Assets/logo.png"), 0.5)
        start_image = pygame.transform.scale_by(pygame.image.load("Assets/start.png"), 0.5)
        bird_image = pygame.transform.rotozoom(pygame.image.load("Assets/flappy_bird.png"), 345, 1.5)
        bird_flap_image = pygame.transform.rotozoom(pygame.image.load("Assets/flappy_bird_1.png"), 25, 1.5)
        score_image = pygame.transform.scale_by(pygame.image.load("Assets/score.png"), 1.5)
        restart_image = pygame.transform.scale_by(pygame.image.load("Assets/restart.png"), 1.5)
        gravity_flip_image = pygame.transform.scale_by(pygame.image.load("Assets/gravity_flip.png"), 1)
        gravity_flip_description_image = pygame.transform.scale_by(pygame.image.load("Assets/gravity_flip_description.png"), 0.75)
        background_pipe_image = pygame.image.load("Assets/background_pipe.png").convert()
        music = pygame.mixer.music.load("Assets/music.mp3")
        pygame.mixer.music.play(loops=-1) # Play background music indefinitely
        file = open("Assets/data.txt")
        score = file.read().split(' ')
        file.close()
        break  # Exit loop if assets are loaded successfully
    except Exception as e:
        # If assets are not loaded, prompt users to download them
        if os.name == 'nt':
            # Message box for Windows systems
            import ctypes
            result = ctypes.windll.user32.MessageBoxW(
                0,
                f"""A software update is required. Update data will be downloaded now. (8.10 MB)""",
                "Flappy Bird",
                0x00000001 | 0x00000010 # MB_OKCANCEL | MB_ICONERROR
            )
        else:
            # Message box for POSIX (macOS/Linux)
            app = NSApplication.sharedApplication()
            app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
            alert = NSAlert.alloc().init()
            alert.setMessageText_("Flappy Bird")
            alert.setInformativeText_(f"""A software update is required. Update data will be downloaded now. (8.10 MB)""")
            alert.addButtonWithTitle_("Download")
            alert.addButtonWithTitle_("Cancel")
            app.activateIgnoringOtherApps_(True)
            result = alert.runModal()
        if result == 1 or result == 1000:  # If user clicks 'Download'
            # URLs for downloading assets
            urls = {"Assets/background.png": "https://deaconlam.github.io/downloads/background.png",
            "Assets/flappy-font.ttf": "https://deaconlam.github.io/downloads/flappy-font.ttf",
            "Assets/flappy_bird.png": "https://deaconlam.github.io/downloads/flappy_bird.png",
            "Assets/flappy_bird_1.png": "https://deaconlam.github.io/downloads/flappy_bird_1.png",
            "Assets/icon.png": "https://deaconlam.github.io/downloads/icon.png",
            "Assets/logo.png": "https://deaconlam.github.io/downloads/logo.png",
            "Assets/restart.png": "https://deaconlam.github.io/downloads/restart.png",
            "Assets/score.png": "https://deaconlam.github.io/downloads/score.png",
            "Assets/start.png": "https://deaconlam.github.io/downloads/start.png",
            "Assets/gravity_flip.png": "https://deaconlam.github.io/downloads/gravity_flip.png",
            "Assets/background_pipe.png": "https://deaconlam.github.io/downloads/background_pipe.png",
            "Assets/gravity_flip_description.png": "https://deaconlam.github.io/downloads/gravity_flip_description.png",
            "Assets/music.mp3": "https://deaconlam.github.io/downloads/music.mp3"
        }
            def download_files():
                # Download files and update UI with a loading bar
                global current_progress
                if os.path.isdir('Assets') == False:
                    os.mkdir('Assets') # Create 'Assets' directory if it doesn't exist
                with open("Assets/data.txt", "x") as file:
                    file.write("0 0") # Initialize data.txt with scores
                progress_step = 100 / 13 # Calculate progress step for each file
                current_progress = 0
                for filename, url in urls.items():
                    try:
                        response = requests.get(url)
                        if response.status_code == 200:
                            with open(filename, "wb") as f:
                                f.write(response.content) # Write downloaded content to file
                    except PermissionError:
                        continue # Skip if permission error occurs
                    except Exception as e:
                        if os.name == 'nt':
                            ctypes.windll.user32.MessageBoxW(
                            0,
                            f"This item is no longer available.",
                            "Flappy Bird",
                            0x00000001 | 0x00000010
                            )
                            continue
                    current_progress += progress_step
                    progress_var.set(current_progress) # Update progress bar
                    progress_label.config(text=f"Downloading game file: {filename} ({int(1 + (current_progress / (100 / 13)))} of 14)")
                    root.update_idletasks() # Refresh Tkinter window
                progress_label.config(text="")
                root.destroy() # Close Tkinter window after download
            def start_download():
                threading.Thread(target=download_files).start() # Start download in a new thread
            if os.name == 'nt':
                # Tkinter GUI for Windows download progress
                root = tk.Tk()
                root.title(f"Downloading file...")
                root.geometry("400x100")
                root.resizable(False, False)
                progress_label = tk.Label(root, text="Downloading game file", font=("Segoe UI", 10), anchor="w", justify="left")
                progress_label.pack(pady=10, fill="x", padx=23)
                progress_var = tk.DoubleVar()
                progress_bar = ttk.Progressbar(root, maximum=100, length=350, variable=progress_var)
                progress_bar.pack(pady=5)
                start_download()
                root.mainloop()
            else:
                # Cocoa (AppKit) GUI for macOS download progress
                class AppDelegate(NSObject):
                    def stopApp_(self, _):
                        progress_bar.stopAnimation_(None)
                        window.close()
                        app.stop_(None)
                delegate = AppDelegate.alloc().init()
                def posix_download():
                    global not_found
                    not_found = 0
                    if not os.path.isdir('Assets'):
                        os.mkdir('Assets')
                    with open("Assets/data.txt", "w") as file:
                        file.write("0 0")
                    for filename, url in urls.items():
                        try:
                            response = requests.get(url)
                            if response.status_code == 200:
                                with open(filename, "wb") as f:
                                    f.write(response.content)
                            else:
                                os.system('clear')
                                not_found = 1
                                break
                        except PermissionError:
                            continue
                    delegate.performSelectorOnMainThread_withObject_waitUntilDone_(
                        "stopApp:", None, False
                    )
                app = NSApplication.sharedApplication()
                app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
                NSRunningApplication.currentApplication().activateWithOptions_(
                    NSApplicationActivateIgnoringOtherApps
                )
                rect = NSMakeRect(0, 0, 400, 100)
                window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                    rect,
                    NSWindowStyleMaskTitled,
                    NSBackingStoreBuffered,
                    False
                )
                window.setTitle_("Downloading file...")
                window.center()
                window.makeKeyAndOrderFront_(None)
                progress_bar = NSProgressIndicator.alloc().initWithFrame_(NSMakeRect(50, 40, 300, 20))
                progress_bar.setIndeterminate_(True) # Indeterminate progress bar
                progress_bar.setStyle_(0) # Set style to spinning
                progress_bar.startAnimation_(None)
                window.contentView().addSubview_(progress_bar)
                thread = threading.Thread(target=posix_download)
                thread.start()
                app.run() # Run the Cocoa application event loop
                if not_found == 1:
                    app = NSApplication.sharedApplication()
                    app.setActivationPolicy_(NSApplicationActivationPolicyRegular)
                    alert = NSAlert.alloc().init()
                    alert.setMessageText_("Flappy Bird")
                    alert.setInformativeText_(f"This item is no longer available.")
                    alert.addButtonWithTitle_("Close")
                    app.activateIgnoringOtherApps_(True)
                    alert.runModal()
                    pygame.quit()
                    os.system('clear')
                    sys.exit()
        elif result == 2 or result == 1001: # If user clicks 'Cancel'
            pygame.quit()
            os.system('cls' if os.name == 'nt' else 'clear') # Clear console
            sys.exit() # Exit the game
            break

# Game state variables
scroll = 0 # Background scroll position
status = 0 # Game status: 0-start, 1-playing, 2-game over
gravity_flip_wave = 0 # Timestamp for gravity flip event
gravity_flip_timer = 10 # Timer for gravity flip mode
sub_gravity_flip_timer = 0 # Sub-timer for gravity flip countdown
substatus = 0 # Sub-status for gravity modes: 0-normal, 1-invulnerable, 2-flipped gravity
score[0] = 0 # Current score
os.system('cls' if os.name == 'nt' else 'clear') # Clear console
start_text_visibility = True # Controls visibility of "Press Space to Start" text
last_saved_time = 0 # Timestamp for last start text toggle
bird_y = (HEIGHT / 2) - (bird_image.get_height() / 2) # Initial bird Y position
flap_timer = 10 # Timer for bird flapping animation
flap_duration = 100 # Duration of bird flap animation
score_delay = 0 # Delay for score increment to prevent rapid scoring
current_bird_image = bird_image # Current bird image to display
cheat = 0 # Cheat mode flag (for invulnerable mode)
invulnerable_mode_timer = 5 # Timer for invulnerable mode
running = True # Flag to keep the game loop running

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Exit game if close button is pressed
        # Check for restart button click in game over screen
        if event.type == pygame.MOUSEBUTTONDOWN and status == 2 and pygame.mouse.get_pos()[0] > (WIDTH - restart_image.get_width()) // 2 and pygame.mouse.get_pos()[0] < ((WIDTH - restart_image.get_width()) // 2 + restart_image.get_width()) and pygame.mouse.get_pos()[1] > (HEIGHT // 2) - restart_image.get_height() // 2 + 250 and pygame.mouse.get_pos()[1] < (HEIGHT // 2) - restart_image.get_height() // 2 + 250 + restart_image.get_height():
            status = 0 # Reset game status to start screen
            scroll = 0 # Reset background scroll
            substatus = 0 # Reset gravity substatus
            pipe_background_started = False # Reset pipe background flag (unused in provided code)
            gravity_flip_wave = pygame.time.get_ticks() # Reset gravity flip timer
            score[0] = 0 # Reset score
            score_delay = 0 # Reset score delay
            bird_y = (HEIGHT / 2) - (bird_image.get_height() / 2) # Reset bird position
    keys = pygame.key.get_pressed() # Get all pressed keys
    # Start game when space is pressed from start screen
    if status == 0 and keys[pygame.K_SPACE]:
        status = 1 # Change game status to playing
        gravity_flip_wave = pygame.time.get_ticks() # Initialize gravity flip timer
    # Bird movement in normal gravity mode
    if status == 1 and (substatus == 0 or substatus == 1) and keys[pygame.K_SPACE] and bird_y >= 0:
        bird_y -= 40 # Move bird up
        flap_timer = pygame.time.get_ticks() # Reset flap animation timer
    # Bird movement in flipped gravity mode
    if status == 1 and substatus == 2 and keys[pygame.K_SPACE] and bird_y < (bg_height - bird_image.get_height()):
        bird_y += 40 # Move bird down
        flap_timer = pygame.time.get_ticks() # Reset flap animation timer

    # Game logic for start screen
    if status == 0:
        # Scroll background continuously
        if scroll < bg_width:
            DISPLAYSURF.blit(bg_image, (-scroll, 0))
            DISPLAYSURF.blit(background_pipe_image, (bg_width - scroll, 0))
        else:
            scroll_pipe = scroll - bg_width
            pipe_count = math.ceil(WIDTH / bg_width) + 2
            for i in range(pipe_count):
                x = i * bg_width - (scroll_pipe % bg_width)
                DISPLAYSURF.blit(background_pipe_image, (x, 0))
        pygame.mouse.set_cursor(*pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)) # Set mouse cursor to arrow
        DISPLAYSURF.blit(bg_image, (0, 0)) # Draw static background for start screen
        DISPLAYSURF.blit(logo_image, ((WIDTH - logo_image.get_width()) // 2, (HEIGHT // 2) - logo_image.get_height() // 2 - 100)) # Draw game logo
        # Toggle visibility of "Press Space to Start" text
        if pygame.time.get_ticks() - last_saved_time > 750:
            start_text_visibility = not start_text_visibility
            last_saved_time = pygame.time.get_ticks()
        if start_text_visibility:
            DISPLAYSURF.blit(start_image, ((WIDTH - start_image.get_width()) // 2, HEIGHT - start_image.get_height() - 205))

    # Game update logic (only if playing)
    if status == 1:
        # Increment score if background color is not black (meaning pipes are present) and delay has passed
        if tuple(DISPLAYSURF.get_at((WIDTH // 2 - 100, 10)))[0] != 0 and (pygame.time.get_ticks() - score_delay) > 2000:
            score[0] += 1
            score_delay = pygame.time.get_ticks()
        scroll_speed = 5 # Set background scroll speed
        # Scroll background continuously
        if scroll < bg_width:
            DISPLAYSURF.blit(bg_image, (-scroll, 0))
            DISPLAYSURF.blit(background_pipe_image, (bg_width - scroll, 0))
        else:
            scroll_pipe = scroll - bg_width
            pipe_count = math.ceil(WIDTH / bg_width) + 2
            for i in range(pipe_count):
                x = i * bg_width - (scroll_pipe % bg_width)
                DISPLAYSURF.blit(background_pipe_image, (x, 0))
        scroll += scroll_speed # Update scroll position

        # Collision detection (only if not in cheat/invulnerable mode)
        if cheat == 0:
            bird_rect = pygame.Rect(
                (WIDTH - current_bird_image.get_width()) // 2,
                int(bird_y),
                current_bird_image.get_width(),
                current_bird_image.get_height()
            )
            # Check pixels around the bird for collision with pipe color
            for x in range(bird_rect.left, bird_rect.right):
                for y in range(bird_rect.top, bird_rect.bottom):
                    try:
                        color = DISPLAYSURF.get_at((x, y))
                        if color[:3] == (37, 49, 39): # Check if color matches pipe color
                            status = 2 # Game over
                    except IndexError:
                        continue # Ignore index errors (out of screen bounds)

        # Normal gravity mode
        if substatus == 0:
            cheat = 0 # Disable cheat mode
            bird_y += 15 # Apply gravity
            # Bird flap animation
            if pygame.time.get_ticks() - flap_timer < flap_duration:
                current_bird_image = bird_flap_image
            else:
                current_bird_image = bird_image
            if bird_y > (bg_height - bird_image.get_height()):
                status = 2 # Game over if bird goes off screen
            else:
                DISPLAYSURF.blit(font.render(str(score[0]), True, (255, 255, 255)), (50, 50)) # Display current score
            # Activate invulnerable mode after 10 seconds
            if pygame.time.get_ticks() - gravity_flip_wave > 10000:
                gravity_flip_wave = pygame.time.get_ticks()
                substatus = 1 # Change to invulnerable substatus
                sub_gravity_flip_timer = pygame.time.get_ticks()

        # Invulnerable mode
        if substatus == 1:
            cheat = 1 # Enable cheat mode (no collision)
            if bird_y < (bg_height - bird_image.get_height()):
                bird_y += 15 # Apply gravity (still goes down)
            else:
                DISPLAYSURF.blit(font.render(str(score[0]), True, (255, 255, 255)), (50, 50)) # Display current score
            # Bird flap animation
            if pygame.time.get_ticks() - flap_timer < flap_duration:
                current_bird_image = bird_flap_image
            else:
                current_bird_image = bird_image
            DISPLAYSURF.blit(gravity_flip_image, ((WIDTH - gravity_flip_image.get_width()) // 2, (HEIGHT // 2) - gravity_flip_image.get_height() // 2 - 50)) # Display gravity flip icon
            DISPLAYSURF.blit(gravity_flip_description_image, ((WIDTH - gravity_flip_description_image.get_width()) // 2, (HEIGHT // 2) - gravity_flip_description_image.get_height() // 2 + 100)) # Display gravity flip description
            # Transition to flipped gravity mode after 5 seconds
            if pygame.time.get_ticks() - gravity_flip_wave > 5000:
                substatus = 2 # Change to flipped gravity substatus
                sub_gravity_flip_timer = pygame.time.get_ticks()
                invulnerable_mode_timer = 5 # Reset invulnerable mode timer
            DISPLAYSURF.blit(font.render("INVULNERABLE MODE", True, (255, 255, 255)), (50, 50)) # Display "INVULNERABLE MODE" text
            DISPLAYSURF.blit(font.render(f"00:{invulnerable_mode_timer:02}", True, (255, 255, 255)), (WIDTH - 300, 50)) # Display invulnerable mode countdown
            # Update invulnerable mode countdown
            if (pygame.time.get_ticks() - sub_gravity_flip_timer) > 1000 and invulnerable_mode_timer > 0:
                invulnerable_mode_timer -= 1
                sub_gravity_flip_timer = pygame.time.get_ticks()

        # Flipped gravity mode
        if substatus == 2:
            cheat = 0 # Disable cheat mode
            bird_y -= 15 # Apply inverted gravity (bird goes up)
            # Bird flap animation (inverted animation)
            if pygame.time.get_ticks() - flap_timer < flap_duration:
                current_bird_image = bird_image # Display normal bird
            else:
                current_bird_image = bird_flap_image # Display flapping bird
            if bird_y < 0:
                status = 2 # Game over if bird goes off screen
            else:
                DISPLAYSURF.blit(font.render(str(score[0]), True, (255, 255, 255)), (50, 50)) # Display current score
                DISPLAYSURF.blit(font.render(f"00:{gravity_flip_timer:02}", True, (255, 255, 255)), (WIDTH - 300, 50)) # Display flipped gravity countdown
            # Update flipped gravity countdown
            if (pygame.time.get_ticks() - sub_gravity_flip_timer) > 1000 and gravity_flip_timer > 0:
                gravity_flip_timer -= 1
                sub_gravity_flip_timer = pygame.time.get_ticks()
            # Return to normal gravity mode after timer
            if gravity_flip_timer == 0:
                substatus = 0 # Change to normal substatus
                gravity_flip_wave = pygame.time.get_ticks() # Reset gravity flip timer
                bird_y = (HEIGHT / 2) - (bird_image.get_height() / 2) # Reset bird position
                gravity_flip_timer = 10 # Reset flipped gravity timer
        DISPLAYSURF.blit(current_bird_image, ((WIDTH - current_bird_image.get_width()) // 2, bird_y)) # Draw the bird

    # Game over logic
    if status == 2:
        # Save high score
        file = open('Assets/data.txt', 'w')
        if int(score[0]) > int(score[1]):
            file.write(f"{score[0]} {score[0]}") # Save current score as high score if it's higher
        else:
            file.write(f"{score[0]} {score[1]}") # Otherwise, save current score and previous high score
        file.close()
        # Reload scores to display
        file = open("Assets/data.txt")
        score = file.read().split(' ')
        file.close()
        DISPLAYSURF.blit(score_image, ((WIDTH - score_image.get_width()) // 2, (HEIGHT // 2) - score_image.get_height() // 2 - 100)) # Display score board image
        DISPLAYSURF.blit(font.render(str(score[0]), True, (255, 255, 255)), (WIDTH // 2 - 25, (HEIGHT // 2) - score_image.get_height() // 2 + 50)) # Display current score
        DISPLAYSURF.blit(font.render(str(score[0] if int(score[0]) > int(score[1]) else str(score[1])), True, (255, 255, 255)), (WIDTH // 2 - 25, (HEIGHT // 2) - score_image.get_height() // 2 + 250)) # Display high score
        DISPLAYSURF.blit(restart_image, ((WIDTH - restart_image.get_width()) // 2, (HEIGHT // 2) - restart_image.get_height() // 2 + 250)) # Display restart button
        # Change mouse cursor to hand when hovering over restart button
        if pygame.mouse.get_pos()[0] > (WIDTH - restart_image.get_width()) // 2 and pygame.mouse.get_pos()[0] < ((WIDTH - restart_image.get_width()) // 2 + restart_image.get_width()) and pygame.mouse.get_pos()[1] > (HEIGHT // 2) - restart_image.get_height() // 2 + 250 and pygame.mouse.get_pos()[1] < (HEIGHT // 2) - restart_image.get_height() // 2 + 250 + restart_image.get_height():
            pygame.mouse.set_cursor(*pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        else:
            pygame.mouse.set_cursor(*pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    pygame.display.flip() # Update the full display Surface to the screen
    clock.tick(60) # Cap the frame rate at 60 FPS
pygame.quit() # Uninitialize pygame modules