import pygame

# Define the cooldown times for each gun (in seconds)
SHOTGUN_COOLDOWN = 0.4
SNIPER_COOLDOWN = 3.0
ASSAULT_RIFLE_COOLDOWN = 0.7

# Define the available guns and their keybinds
guns = {
    'fists': {'pullout_cooldown': 0, 'fire_cooldown': 10000000000, 'keybind': pygame.K_1},
    'shotgun': {'pullout_cooldown': 0, 'fire_cooldown': SHOTGUN_COOLDOWN, 'keybind': pygame.K_f},
    'sniper': {'pullout_cooldown': 0, 'fire_cooldown': SNIPER_COOLDOWN, 'keybind': pygame.K_LSHIFT},
    'assault rifle': {'pullout_cooldown': 0, 'fire_cooldown': ASSAULT_RIFLE_COOLDOWN, 'keybind': pygame.K_SPACE}
}

# Store the original cooldowns for each gun
original_cooldowns = {gun: guns[gun]['fire_cooldown'] for gun in guns}

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create a Pygame window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Gun Cooldown")

# Create a font for displaying text
font = pygame.font.Font(None, 36)

# Variable to store the active gun
active_gun = 'fists'

# Variable to store the previously active gun
previous_gun = None

# Variable to track if the gun has been pulled out
gun_pulled_out = False

# Function to simulate pulling out a gun
def pullout_gun(gun):
    global active_gun, previous_gun, gun_pulled_out
    if guns[gun]['pullout_cooldown'] <= 0:
        print(f"Pulling out {gun}!")
        guns[gun]['pullout_cooldown'] = guns[gun]['fire_cooldown']
        previous_gun = active_gun
        active_gun = gun
        gun_pulled_out = True
        # Reset the fire cooldown of all guns except the active gun
        for other_gun in guns:
            if other_gun != active_gun:
                guns[other_gun]['fire_cooldown'] = original_cooldowns[other_gun]
    else:
        print(f"{gun} is on cooldown. Please wait.")

# Function to simulate firing a gun
def fire_gun(gun):
    global gun_pulled_out
    if not gun_pulled_out:
        print(f"{gun} is not pulled out yet. Pull out the gun first.")
    elif guns[gun]['fire_cooldown'] <= 0:
        print(f"Firing {gun}!")
        guns[gun]['fire_cooldown'] = original_cooldowns[gun]  # Reset the fire cooldown after firing
    else:
        print(f"{gun} is on cooldown. Please wait.")


# Main program loop
running = True
clock = pygame.time.Clock()
while running:
    # Limit frame rate
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            for gun in guns:
                if event.key == guns[gun]['keybind']:
                    if gun != active_gun:
                        pullout_gun(gun)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for gun in guns:
                    if guns[gun]['fire_cooldown'] <= 0 and gun_pulled_out:
                        fire_gun(gun)


    # Update the pullout cooldowns for each gun
    for gun in guns:
        if gun_pulled_out or gun == active_gun:
            if guns[gun]['pullout_cooldown'] > 0:
                guns[gun]['pullout_cooldown'] -= 0.1  # Decrease the pullout cooldown by 0.1 seconds

    # Update the fire cooldown for the active gun
    if gun_pulled_out:
        if guns[active_gun]['fire_cooldown'] > 0:
            guns[active_gun]['fire_cooldown'] -= 0.1  # Decrease the fire cooldown by 0.1 seconds

    # Display the active gun
    window.fill((0, 0, 0))
    gun_text = font.render(f"Active Gun: {active_gun.capitalize()}", True, WHITE)
    gun_text_rect = gun_text.get_rect(left=20, top=100)
    window.blit(gun_text, gun_text_rect)

    # Display the cooldown for the active gun
    active_cooldown = guns[active_gun]['fire_cooldown']
    cooldown_text = f"{active_gun.capitalize()} Cooldown: {max(active_cooldown, 0):.1f}s"
    cooldown_render = font.render(cooldown_text, True, WHITE)
    cooldown_rect = cooldown_render.get_rect(left=20, top=200)

    # Adjust the position of the cooldown text if it goes beyond the window height
    if cooldown_rect.bottom > window_height:
        cooldown_rect.top -= cooldown_rect.bottom - window_height + 10

    # Display the active gun and its cooldown
    window.fill((0, 0, 0))
    gun_text = font.render(f"Active Gun: {active_gun.capitalize()}", True, WHITE)
    gun_text_rect = gun_text.get_rect(left=20, top=100)
    window.blit(gun_text, gun_text_rect)
    window.blit(cooldown_render, cooldown_rect)



    # Update the display
    pygame.display.flip()

# Quit the program
pygame.quit()
print("Program exited.")
