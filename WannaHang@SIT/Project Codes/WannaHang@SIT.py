import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import pygame
import os   
from PIL import Image, ImageTk  # Import for handling images

"""
READ ME FIRST:
WE LOVE OUR PROJECT!!!


NEED TO INSTALL:
pygame into your system, --> You can install by doing: python3 -m pip install pygame
PIL into your system --> You can install by doing: python3 -m pip install pillow
After that this code is able to run :)

"""
#Update a music background and settings page (added music volume)
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        pygame.mixer.init() #Initialize the mixer for sound
        
        self.title("WannaHang@SIT")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.configure(bg="#2C3E50") #2C3E50
        self.user_data = {}  # Dictionary to store session data
        self.lives = 10  # Shared lives among all topics
        self.completed_topics = set()  # Keep track of completed topics
        self.completion_message_displayed = False
        self.hints_enabled = tk.BooleanVar(value=True)  # Initialize with hints enabled by default
        self.current_music = None

        #Define part for complete music
        base_dir2 = os.path.dirname(os.path.abspath(__file__))
        self.complete_sound_file = os.path.join(base_dir2, 'Sound', 'Complete.mp3')




  
        # Load the hangman images and store them in a list
        self.hangman_images = []
        for i in range(1, 11):  # Assuming images are named Hangman # 1.jpg to Hangman # 10.jpg
            image_path = os.path.join(os.path.dirname(__file__), 'Images', f"Hangman #{i}.jpg")
            image = Image.open(image_path)
            image = image.resize((250, 332), Image.Resampling.LANCZOS)  # Resize the image to fit the display
            self.hangman_images.append(ImageTk.PhotoImage(image))  # Store the resized image

        # Define custom fonts
        self.title_font = tkfont.Font(family='Arial', size=48, weight="bold")
        self.topic_font = tkfont.Font(family='Arial', size=36, weight="bold")
        self.subtitle_font = tkfont.Font(family='Arial', size=36, weight="bold")
        self.button_font = tkfont.Font(family='Arial', size=18)
        self.label_font = tkfont.Font(family='Arial', size=16)
        self.question_font = tkfont.Font(family='Arial', size=20)  # Font for the question test commit 2,3

        self.frames = {}
        # Create a container for all pages test
        container = tk.Frame(self, bg="#2C3E50")
        container.pack(side="top", fill="both", expand=True)

        # Dictionary to hold references to the pages

        for F in (StartPage, LoginPage, TopicSelectPage, RulesPage, SettingsPage,
                Maths1Page, ProgrammingFundamentalsPage, IntroToComputingPage,
                ComputerOrganizationAndArchitecturePage, CompletionPage):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.play_background_music()
        self.show_frame(StartPage)

    def refresh_lives(self):
        self.lives_label.config(text=f"Lives: {self.controller.lives}")
        hearts = '❤️' * self.controller.lives  # Create the hearts string
        self.hearts_label.config(text=hearts)  # Update the hearts display

    def show_frame(self, page):
        """Bring the specified page to the front."""
        frame = self.frames[page]
        frame.tkraise()

        # Reset the game if navigating to a specific game page
        if page in [Maths1Page, ProgrammingFundamentalsPage, IntroToComputingPage, ComputerOrganizationAndArchitecturePage]:
            frame.reset_game()
        
        # Stop music if navigating to specific game pages
        if isinstance(frame, (Maths1Page, ProgrammingFundamentalsPage, IntroToComputingPage, ComputerOrganizationAndArchitecturePage, HangmanGamePage, CompletionPage)):
            frame.play_current_difficulty_music()
            frame.refresh_lives()  # Refresh lives when showing a new frame
            frame.update_hangman_image()  # Also update the hangman image

        else:
            self.play_background_music()

        # Update the welcome message if on TopicSelectPage
        if page == TopicSelectPage:
            name = self.user_data.get('name', '')
            frame.update_welcome_message(name)
        
                

    def play_background_music(self):
        music_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Sound', 'Background.mp3')
        
        if self.current_music != music_file or not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # Play in a loop
            self.current_music = music_file  # Update current music track

    def stop_music(self):
        """Stop playing music."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.current_music = None  # Reset current music track



    def reset_game(self):
        """Reset the game progress and lives."""
        self.lives = 10
        self.completed_topics.clear()
        self.completion_message_displayed = False
        # Reset HangmanGamePage instances
        for page_class in [Maths1Page, ProgrammingFundamentalsPage, IntroToComputingPage, ComputerOrganizationAndArchitecturePage]:
            self.frames[page_class].reset_game()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2C3E50")
        self.controller = controller
        

        
        label = tk.Label(
            self, text="WannaHang@SIT",
            font=controller.title_font, bg="#2C3E50", fg="#ECF0F1"
        )
        label.pack(pady=(100, 0))

          # Load the left image
        try:
            left_image_path = os.path.join(os.path.dirname(__file__), "Images", f"Introhangmanleft.jpg")
            print(f"Loading right image from: {left_image_path}")
            self.left_image = Image.open(left_image_path)
            self.left_image = self.left_image.resize((150, 273), Image.Resampling.LANCZOS)  # Resize if needed
            self.left_photo = ImageTk.PhotoImage(self.left_image)
        except Exception as e:
            print(f"Error loading left image: {e}")
            return  # If there's an issue loading the image, don't proceed

        # Load the right image
        try:
            right_image_path = os.path.join(os.path.dirname(__file__), "Images", "Introhangmanright.jpg")
            print(f"Loading right image from: {right_image_path}")
            self.right_image = Image.open(right_image_path)
            self.right_image = self.right_image.resize((150, 273), Image.Resampling.LANCZOS)  # Resize if needed
            self.right_photo = ImageTk.PhotoImage(self.right_image)
        except Exception as e:
            print(f"Error loading right image: {e}")
            return  # If there's an issue loading the image, don't proceed

        # Create labels to display the images
        self.left_image_label = tk.Label(self, image=self.left_photo, bg="#2C3E50")
        self.right_image_label = tk.Label(self, image=self.right_photo, bg="#2C3E50")

        # Position the images
        #self.left_image_label.place(relx=0.05, rely=0.5, anchor='w')  # 5% from the left
        #self.right_image_label.place(relx=0.95, rely=0.5, anchor='e')  # 5% from the right

        self.left_image_label.pack(side="left", padx=100, pady=10)
        self.right_image_label.pack(side="right", padx=100, pady=10)

        # Spacer to push buttons lower
        spacer = tk.Frame(self, height=200, bg="#2C3E50")
        spacer.pack()

        # Start Button
        start_button = tk.Button(
            self, text="Start", font=controller.button_font,
            command=lambda: controller.show_frame(LoginPage),
            bg="#3498DB", fg="#ECF0F1", width=20, height=2,
            relief='flat', bd=0, activebackground="#2980B9"
        )
        start_button.pack(pady=10)

        # Quit Button
        quit_button = tk.Button(
            self, text="Quit", font=controller.button_font,
            command=self.quit_app,
            bg="#C0392B", fg="#ECF0F1", width=20, height=2,
            relief='flat', bd=0, activebackground="#A93226"
        )
        quit_button.pack(pady=10)

    def quit_app(self):
        """Prompt the user to confirm quitting the app."""
        answer = messagebox.askyesno(
            "Quit Application",
            "Are you sure you want to quit? Your progress will not be saved."
        )
        if answer:
            self.controller.destroy()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2C3E50")
        self.controller = controller

        label = tk.Label(
            self, text="Login",
            font=controller.title_font, bg="#2C3E50", fg="#ECF0F1"
        )
        label.pack(pady=(50, 20))

        # Create a frame for the form
        form_frame = tk.Frame(self, bg="#2C3E50")
        form_frame.pack()

        # Name Field
        name_label = tk.Label(
            form_frame, text="Name:", font=controller.label_font,
            bg="#2C3E50", fg="#ECF0F1"
        )
        name_label.pack(anchor='w')
        self.name_entry = tk.Entry(form_frame, font=controller.label_font, width=30)
        self.name_entry.pack(pady=(0, 10))

        # Email Field
        email_label = tk.Label(
            form_frame, text="SIT Email:", font=controller.label_font,
            bg="#2C3E50", fg="#ECF0F1"
        )
        email_label.pack(anchor='w')
        self.email_entry = tk.Entry(form_frame, font=controller.label_font, width=30)
        self.email_entry.pack(pady=(0, 10))

        # Login Button
        login_button = tk.Button(
            self, text="Login", font=controller.button_font,
            command=self.validate_login,
            bg="#E74C3C", fg="#ECF0F1", width=15, height=1,
            relief='flat', bd=0, activebackground="#C0392B"
        )
        login_button.pack(pady=30)

        # Quit Button at the bottom left
        quit_button = tk.Button(
            self, text="Quit", font=controller.button_font,
            command=self.quit_app,
            bg="#C0392B", fg="#ECF0F1", width=10, height=1,
            relief='flat', bd=0, activebackground="#A93226"
        )
        quit_button.place(relx=0.05, rely=0.95, anchor='sw')

    def validate_login(self):
        """Validate the name and email fields."""
        name = self.name_entry.get()
        email = self.email_entry.get()

        if not name.strip():
            messagebox.showerror("Input Error", "Name cannot be empty.")
            return
        if not email.strip():
            messagebox.showerror("Input Error", "Email cannot be empty.")
            return
        if '@' not in email:
            messagebox.showerror("Input Error", "Invalid email address.")
            return

        # Store user data
        self.controller.user_data['name'] = name
        self.controller.user_data['email'] = email
        
        self.controller.reset_game()
        self.controller.show_frame(TopicSelectPage)

    def quit_app(self):
        """Prompt the user to confirm quitting the app."""
        answer = messagebox.askyesno(
            "Quit Application",
            "Are you sure you want to quit? Your progress will not be saved."
        )
        if answer:
            self.controller.destroy()

class TopicSelectPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2C3E50")
        self.controller = controller

        # Welcome Message (will be updated later)
        self.welcome_label = tk.Label(
            self, text="", font=controller.label_font,
            bg="#2C3E50", fg="#ECF0F1"
        )
        self.welcome_label.place(relx=0.05, rely=0.05, anchor='nw')

        # Completion Message (will be shown when all topics are completed)
        self.completion_message = tk.Label(
            self, text="", font=controller.label_font,
            bg="#2C3E50", fg="#ECF0F1"
        )
        self.completion_message.place(relx=0.5, rely=0.05, anchor='n')

        # Lives Left Label
        self.lives_label = tk.Label(
            self, text="", font=controller.label_font,
            bg="#2C3E50", fg="#ECF0F1"
        )
        self.lives_label.place(relx=0.05, rely=0.1, anchor='nw')

        # Create a frame to center the content
        content_frame = tk.Frame(self, bg="#2C3E50")
        content_frame.place(relx=0.5, rely=0.5, anchor='center')

        label = tk.Label(
            content_frame, text="Select a Topic",
            font=controller.title_font, bg="#2C3E50", fg="#ECF0F1"
        )
        label.pack(pady=20)

        self.topics = [
            "Maths 1",
            "Programming Fundamentals",
            "Intro to Computing",
            "Computer Org and Arch"
        ]

        self.topic_pages = {
            "Maths 1": Maths1Page,
            "Programming Fundamentals": ProgrammingFundamentalsPage,
            "Intro to Computing": IntroToComputingPage,
            "Computer Org and Arch": ComputerOrganizationAndArchitecturePage
        }

        self.button_frame = tk.Frame(content_frame, bg="#2C3E50")
        self.button_frame.pack()

        self.create_topic_buttons()

        # 'Rules' Button at the bottom right
        rules_button = tk.Button(
            self, text="Rules", font=controller.button_font,
            command=lambda: controller.show_frame(RulesPage),
            bg="#E67E22", fg="#ECF0F1", width=10, height=1,
            relief='flat', bd=0, activebackground="#D35400"
        )
        # Place the 'Rules' button at the bottom right
        rules_button.place(relx=0.95, rely=0.95, anchor='se')
        
        
        #Settings:
        Setting_button = tk.Button(
            self, text="Settings", font=controller.button_font,
            command=lambda: controller.show_frame(SettingsPage),
            bg="#3498DB", fg="#ECF0F1", width=10, height=1,  # Adjusted height
            relief='flat', bd=0, activebackground="#2980B9"
        )
        
        Setting_button.place(relx=0.95, rely=0.05, anchor='ne')
        
        
        # 'Quit App' Button at the bottom left
        quit_button = tk.Button(
            self, text="Quit App", font=controller.button_font,
            command=self.quit_app,
            bg="#C0392B", fg="#ECF0F1", width=10, height=1,
            relief='flat', bd=0, activebackground="#A93226"
        )
        # Place the 'Quit App' button at the bottom left
        quit_button.place(relx=0.05, rely=0.95, anchor='sw')

    def update_welcome_message(self, name):
        """Update the welcome message with the user's name and lives left."""
        self.welcome_label.config(text=f"Welcome, {name}!")
        self.lives_label.config(text=f"Lives Left: {self.controller.lives}❤️")
        self.refresh_topic_buttons()
        # Show completion message if all topics are completed
        if len(self.controller.completed_topics) == len(self.topics) and not self.controller.completion_message_displayed:
            self.completion_message.config(text="Congrats for completing this quiz, you have won a $20 voucher which will be emailed to you shortly.")
            self.controller.completion_message_displayed = True
            self.play_completion_music()
        else:
            self.controller.play_background_music()  # Otherwise, play background.mp3

    def play_completion_music(self):
        """Play completion music once all topics are completed."""
        if os.path.exists(self.controller.complete_sound_file):
            pygame.mixer.music.load(self.controller.complete_sound_file)
            pygame.mixer.music.play(-1)  # Loop Complete.mp3
            self.controller.current_music = self.controller.complete_sound_file

    def create_topic_buttons(self):
        """Create topic buttons."""
        self.topic_buttons = {}
        for topic in self.topics:
            button = tk.Button(
                self.button_frame, text=topic, font=self.controller.button_font,
                command=lambda t=topic: self.select_topic(t),
                bg="#16A085", fg="#ECF0F1", width=40, height=2,
                relief='flat', bd=0, activebackground="#138D75"
            )
            button.pack(pady=10)
            self.topic_buttons[topic] = button

    def refresh_topic_buttons(self):
        """Refresh the state of topic buttons based on completion and lives."""
        for topic, button in self.topic_buttons.items():
            if topic in self.controller.completed_topics:
                button.config(
                    text=f"{topic} (Completed)",
                    state='disabled',
                    bg="#95A5A6"
                )
            elif self.controller.lives <= 0:
                button.config(
                    state='disabled',
                    bg="#95A5A6"
                )
            else:
                button.config(
                    text=topic,
                    state='normal',
                    bg="#16A085"
                )

    def select_topic(self, topic):
        """Store the selected topic and proceed to the topic page."""
        self.controller.user_data['topic'] = topic
        # Show the corresponding topic page
        page_class = self.topic_pages[topic]
        self.controller.show_frame(page_class)

    def quit_app(self):
        """Prompt the user to confirm quitting the app."""
        answer = messagebox.askyesno(
            "Quit Application",
            "Are you sure you want to quit? Your progress will not be saved."
        )
        if answer:
            self.controller.destroy()

class RulesPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2C3E50")
        self.controller = controller

        label = tk.Label(
            self, text="Rules",
            font=controller.title_font, bg="#2C3E50", fg="#ECF0F1"
        )
        label.pack(pady=(50, 20))

        # Updated Rules content
        rules_text = (
            "Welcome to the Hangman Quiz!\n\n"
            "You have 10 lives shared across all topics.\n"
            "If you lose all your lives, you'll be returned to the login page, and your progress will be reset.\n\n"
            "Difficulty Levels:\n"
            "- Easy (Question 1): Gain 1 health back after correctly guessing 3 letters.\n"
            "- Medium (Question 2): Gain 1 health back after correctly guessing 4 letters.\n"
            "- Hard (Question 3): Gain 1 health back after correctly guessing 4 letters. A 1-minute timer is active. If the timer runs out, you lose 1 health and the timer resets.\n\n"
            "Complete all the words in a topic to receive a special message!\n\n"
            "Good luck!"
        )

        text_label = tk.Label(
            self, text=rules_text, font=self.controller.label_font,
            bg="#2C3E50", fg="#ECF0F1", wraplength=1000, justify="left"
        )
        text_label.pack(pady=20, padx=20)

        # Back Button at the top left
        back_button = tk.Button(
            self, text="Back", font=controller.button_font,
            command=lambda: controller.show_frame(TopicSelectPage),
            bg="#3498DB", fg="#ECF0F1", width=10, height=1,
            relief='flat', bd=0, activebackground="#2980B9"
        )
        # Place the back button at the top left
        back_button.place(relx=0.05, rely=0.05, anchor='nw')

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2C3E50")
        self.controller = controller
        
        label = tk.Label(
            self, text="Settings",
            font=controller.title_font, bg="#2C3E50", fg="#ECF0F1"
        )
        label.pack(pady=(50, 20))
        
         # Volume Label
        volume_label = tk.Label(
            self, text="Volume:", font=controller.label_font,
            bg="#2C3E50", fg="#ECF0F1"
        )
        volume_label.pack(pady=10)

        # Volume Slider
        self.volume_slider = tk.Scale(
            self, from_=0, to=100, orient="horizontal", length=300,
            bg="#2C3E50", fg="#ECF0F1", highlightthickness=0,
            troughcolor="#3498DB", activebackground="#2980B9",
            font=controller.label_font, command=self.set_volume
        )
        self.volume_slider.set(50)  # Set initial volume to 50%
        self.volume_slider.pack(pady=10)



        # Frame to hold "Enable Hints" label and checkbox side-by-side
        hint_frame = tk.Frame(self, bg="#2C3E50")
        hint_frame.pack(pady=(20, 0))  # Align with volume and adjust vertical spacing
        
        # Enable Hints Label
        hint_label = tk.Label(
            hint_frame, text="Enable Hints:", font=controller.label_font,
            bg="#2C3E50", fg="#ECF0F1"
        )
        hint_label.pack(side="left")  # Adjust padding as needed

        # Enable Hints Checkbox
        self.hint_toggle = tk.Checkbutton(
            hint_frame, variable=controller.hints_enabled,
            bg="#2C3E50", selectcolor="#2C3E50", activebackground="#2C3E50"
        )
        self.hint_toggle.pack(side="left", padx=(10, 0))  # Adjust bottom padding as needed
        

        # Back Button
        back_button = tk.Button(
            self, text="Back", font=controller.button_font,
            command=lambda: controller.show_frame(TopicSelectPage),
            bg="#3498DB", fg="#ECF0F1", width=10, height=1,
            relief='flat', bd=0, activebackground="#2980B9"
        )
        back_button.pack(pady=20)

    def set_volume(self, value):
        """Adjust the music volume based on the slider value."""
        volume = int(value) / 100  # Convert slider value (0-100) to (0.0-1.0)
        pygame.mixer.music.set_volume(volume)
        

   
        


class HangmanGamePage(tk.Frame):
    def __init__(self, parent, controller, topic_name, words_list, questions_list):
        super().__init__(parent, bg="#2C3E50")
        self.controller = controller
        self.topic_name = topic_name
        self.words_list = words_list
        self.questions_list = questions_list
        self.word_index = 0
        self.current_word = self.words_list[self.word_index]
        self.current_question = self.questions_list[self.word_index]  # Get the first question
        self.guessed_letters = set()
        self.incorrect_guesses = set()
        self.timer_id = None
        self.time_left = 60  # 1 minute timer for hard level
        self.life_gained = False
        self.current_difficulty_music = None

        


        # Set the initial hangman image (full lives should show Hangman #1)
        self.hangman_label = tk.Label(self, image=self.controller.hangman_images[0], bg="#2C3E50")
        self.hangman_label.place(relx=0.05, rely=0.6, anchor="w")

        #Define file paths for different difficulty music files
        base_dir1 = os.path.dirname(os.path.abspath(__file__))
        self.music_file_easy = os.path.join(base_dir1, 'Sound', 'EASY.mp3')
        self.music_file_medium = os.path.join(base_dir1, 'Sound', 'Medium.mp3')
        self.music_file_hard = os.path.join(base_dir1, 'Sound', 'Hard.mp3')
        
        # Define path for incorrect sound effect
        self.incorrect_sound_file = os.path.join(base_dir1, 'Sound', 'Incorrect.mp3')
        self.incorrect_sound = pygame.mixer.Sound(self.incorrect_sound_file)
        
        # Define part for correct sound effect
        self.correct_sound_file = os.path.join(base_dir1, 'Sound', 'Correct.mp3')
        self.correct_sound = pygame.mixer.Sound(self.correct_sound_file)



        # Difficulty Levels
        self.difficulty_levels = ["Easy", "Medium", "Hard"]
        self.difficulty_colors = {"Easy": "#27AE60", "Medium": "#F1C40F", "Hard": "#E74C3C"}

        # Title label
        label = tk.Label(
            self, text=self.topic_name,
            font=controller.topic_font, bg="#2C3E50", fg="#ECF0F1",
        )
        label.pack(pady=(20, 10))

        # Level indicator
        self.level_label = tk.Label(
            self, text=f"Level {self.word_index + 1}/3",
            font=controller.button_font, bg="#2C3E50", fg="#ECF0F1"
        )
        self.level_label.place(relx=0.95, rely=0.025, anchor='ne')

        # Difficulty label at the top right
        self.difficulty_label = tk.Label(
            self, text="", font=controller.button_font,
            bg="#2C3E50", fg="#ECF0F1"
        )
        self.difficulty_label.place(relx=0.95, rely=0.06, anchor='ne')

        # Lives label
        self.lives_label = tk.Label(
            self, text=f"❤️: {self.controller.lives}",
            font=controller.label_font, bg="#2C3E50", fg="#ECF0F1"
        )
        self.lives_label.pack(pady=5)

        #Label for the hearts
        self.hearts_label = tk.Label(self, text='❤️' * self.controller.lives, font=controller.label_font, bg="#2C3E50", fg="#ECF0F1")
        self.hearts_label.pack(pady=5)

        # Timer label (added to avoid the AttributeError)
        self.timer_label = tk.Label(
            self, text="", font=controller.label_font,
            bg="#2C3E50", fg="#ECF0F1"
        )
        self.timer_label.pack(pady=5)

        # **Display the actual question**
        self.question_label = tk.Label(
            self, text=self.current_question,  # Display the current question
            font=controller.question_font, bg="#2C3E50", fg="#ECF0F1"
        )
        self.question_label.pack(pady=15)

        # Word display
        self.word_display = tk.Label(
            self, text=self.get_display_word(),
            font=controller.subtitle_font, bg="#2C3E50", fg="#ECF0F1"
        )
        self.word_display.pack(pady=10)

        # Input for guessing letters
        input_frame = tk.Frame(self, bg="#2C3E50")
        input_frame.pack(pady=10)
        self.guess_entry = tk.Entry(input_frame, font=controller.label_font)
        self.guess_entry.pack(side='left', padx=5)
        self.guess_entry.bind("<Return>", self.check_guess_event)  # Bind Enter key
        self.guess_button = tk.Button(
            input_frame, text="Guess", font=controller.button_font,
            command=self.check_guess,
            bg="#E74C3C", fg="#ECF0F1", width=10, height=1,
            relief='flat', bd=0, activebackground="#C0392B"
        )
        self.guess_button.pack(side='left', padx=5)

        # Incorrect guesses display
        self.incorrect_label = tk.Label(
            self, text="Incorrect guesses: ",
            font=controller.label_font, bg="#2C3E50", fg="#ECF0F1"
        )
        self.incorrect_label.pack(pady=5)

        # Next button (initially hidden)
        self.next_button = tk.Button(
            self, text="Next", font=controller.button_font,
            command=self.next_word,
            bg="#27AE60", fg="#ECF0F1", width=10, height=1,
            relief='flat', bd=0, activebackground="#229954"
        )

        # Back Button at the top left
        #back_button = tk.Button(
        #    self, text="Back", font=controller.button_font,
         #   command=self.go_back,
         #   bg="#3498DB", fg="#ECF0F1", width=10, height=1,
        #    relief='flat', bd=0, activebackground="#2980B9"
       # )
        # Place the back button at the top left
       # back_button.place(relx=0.05, rely=0.05, anchor='nw')

        # Set the initial difficulty level
        self.set_difficulty_level()

    def refresh_lives(self):
        
        """Refresh the lives label when switching to this frame."""
        self.lives_label.config(text=f"Lives:{self.controller.lives}",)
        hearts = '❤️' * self.controller.lives  # Create the hearts string
        self.hearts_label.config(text=hearts)  # Update the hearts display


    def check_guess_event(self, event):
        """Handle Enter key press for guess submission."""
        self.check_guess()

    def set_difficulty_level(self):
        """Set the difficulty level based on the current word index."""
        self.life_gained = False
        if self.word_index == 0:
            self.difficulty = "Easy"
            self.current_difficulty_music = self.music_file_easy
        elif self.word_index == 1:
            self.difficulty = "Medium"
            self.current_difficulty_music = self.music_file_medium
        else:
            self.difficulty = "Hard"
            self.current_difficulty_music = self.music_file_hard
        # Update the difficulty label
        self.difficulty_label.config(
            text=self.difficulty,
            fg=self.difficulty_colors[self.difficulty]
        )
        # Update level label
        self.level_label.config(text=f"Level {self.word_index + 1}/3")
        # If hard difficulty, start the timer
        if self.difficulty == "Hard":
            self.start_timer()
        else:
            self.timer_label.config(text="")
            self.stop_timer()
        
        # Play the current difficulty music after setting it
        self.play_current_difficulty_music()
    
        
    def update_hangman_image(self):
        """Update the hangman image based on the current number of lives."""
        current_lives = self.controller.lives
        if 1 <= current_lives <= 10:
            # Invert the index so that 10 lives correspond to Hangman #1 and 1 life corresponds to Hangman #10
            image_index = 10 - current_lives
            self.hangman_label.config(image=self.controller.hangman_images[image_index])  # Update the image


    def play_current_difficulty_music(self):
        """Play music based on the current difficulty level."""
        # Only play the track if it’s not already the current music
        if self.controller.current_music != self.current_difficulty_music:
            self.controller.stop_music()  # Ensure any existing music stops
            pygame.mixer.music.load(self.current_difficulty_music)
            pygame.mixer.music.play(-1)  # Play the music on loop
            self.controller.current_music = self.current_difficulty_music
            



    def start_timer(self):
        """Start or reset the timer for hard difficulty."""
        self.time_left = 60
        self.update_timer()

    def update_timer(self):
        """Update the timer display and handle timeout."""
        mins, secs = divmod(self.time_left, 60)
        time_format = f"Time Left: {mins:02d}:{secs:02d}"
        self.timer_label.config(text=time_format)
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.after(1000, self.update_timer)
            self.refresh_lives()
        else:
            # Timer ran out
            self.controller.lives -= 1
            if self.controller.lives < 0:
                self.controller.lives = 0
            self.lives_label.config(text=f"Lives: {self.controller.lives}")
            if self.controller.lives <= 0:
                self.game_over()
            else:
                messagebox.showinfo("Time's Up!", "You ran out of time and lost a life!")
                self.start_timer()

    def stop_timer(self):
        """Stop the timer if it's running."""
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def get_display_word(self):
        """Returns the word with guessed letters revealed and others as underscores."""
        display_word = ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.current_word])
        return display_word

    def check_guess(self):
        guess = self.guess_entry.get().strip().lower()
        self.guess_entry.delete(0, tk.END)
        if not guess or len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Invalid Input", "Please enter a single alphabetic character.")
            return
        if guess in self.guessed_letters or guess in self.incorrect_guesses:
            messagebox.showinfo("Already Guessed", "You have already guessed that letter.")
            return
        if guess in self.current_word:
            #Play correct sound
            self.correct_sound.play()
            self.guessed_letters.add(guess)
            self.word_display.config(text=self.get_display_word())
            self.refresh_lives()
            # Check for life gain based on difficulty
            if self.controller.lives < 10:
                if self.difficulty == "Easy" and len(self.guessed_letters) == 3 and not self.life_gained:
                    self.controller.lives += 1
                    self.life_gained = True
                    self.refresh_lives()
                elif self.difficulty in ["Medium", "Hard"] and len(self.guessed_letters) == 4 and not self.life_gained:
                    self.controller.lives += 1
                    self.life_gained = True
                    self.refresh_lives()
                if self.controller.lives > 10:
                    self.controller.lives = 10  # Ensure max lives is 10
            self.lives_label.config(text=f"Lives: {self.controller.lives}")

            if all(letter in self.guessed_letters for letter in self.current_word):
                # Disable the Guess button once the word is fully guessed
                self.guess_button.config(state='disabled')
                # Word guessed correctly, directly move to the next without pop-up
                if self.word_index < len(self.words_list) - 1:
                    self.next_button.pack(pady=10)
                    self.incorrect_attempts = 0
                    
                else:
                    self.finish_topic()
        else:
            #play incorrect sound
            self.incorrect_sound.play()
            
            self.controller.lives -= 1
            if self.controller.lives < 0:
                self.controller.lives = 0
            self.lives_label.config(text=f"Lives: {self.controller.lives}")
            self.incorrect_guesses.add(guess)
            self.incorrect_label.config(text=f"Incorrect guesses: {', '.join(sorted(self.incorrect_guesses))}")
            self.update_hangman_image()  # Update the hangman image after losing a life
            self.refresh_lives()

          
            self.incorrect_attempts += 1
            if self.incorrect_attempts == 3 and self.controller.hints_enabled.get(): #Only show hint when hint section is enabled
                self.show_hint()  # Show the hint here
            if self.controller.lives <= 0:
                self.game_over()
                
    def show_hint(self):
        """Show a hint only if hints are enabled."""
        if self.controller.hints_enabled.get(): # Check the toggle state each time
            hint = f"One of the letter is: {self.current_word[3]}"
            messagebox.showinfo("Hint", hint)

    def next_word(self):
        self.word_index += 1
        self.current_word = self.words_list[self.word_index]
        self.current_question = self.questions_list[self.word_index]  # Update the current question
        self.guessed_letters.clear()
        self.incorrect_guesses.clear()
        self.life_gained = False
        self.word_display.config(text=self.get_display_word())
        self.question_label.config(text=self.current_question)  # Update the question display
        self.incorrect_label.config(text="Incorrect guesses: ")
        self.next_button.pack_forget()
        self.set_difficulty_level()
        self.guess_button.config(state='normal')

    def finish_topic(self):
        self.stop_timer()
        self.controller.completed_topics.add(self.topic_name)
        if len(self.controller.completed_topics) == len(self.controller.frames) - 6:  # 6 non-topic pages
            self.controller.show_frame(CompletionPage)
        else:
            self.controller.show_frame(TopicSelectPage)
        self.controller.frames[TopicSelectPage].refresh_topic_buttons()

    def game_over(self):
        self.stop_timer()
        messagebox.showinfo("Game Over", "You lost all your lives, please try again.")
        self.controller.reset_game()
        self.controller.show_frame(LoginPage)

    def go_back(self):
        self.stop_timer()
        self.controller.show_frame(TopicSelectPage)
        

    def reset_game(self):
        """Reset the game state."""
        self.word_index = 0
        self.current_question = self.questions_list[self.word_index]
        self.current_word = self.words_list[self.word_index]
        self.guessed_letters.clear()
        self.incorrect_guesses.clear()
        self.stop_timer()
        self.life_gained = False
        self.lives_label.config(text=f"Lives: {self.controller.lives}")
        self.word_display.config(text=self.get_display_word())
        self.incorrect_label.config(text="Incorrect guesses: ")
        self.next_button.pack_forget()
        self.set_difficulty_level()
        self.guess_button.config(state='normal')  # Ensure the "Guess" button is enabled
        self.question_label.config(text=self.current_question)

class CompletionPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2C3E50")
        self.controller = controller

        # Get the user's name from the stored user data
        #name = controller.user_data.get('name')  # Default to 'Player' if no name is available. NOT WORKING!

        # Congrats label in the center, with the user's name
        self.label = tk.Label(
            self, text=f"Congrats! You have won a $20 grab voucher. An email will be sent out shortly. 🎉", 
            font=controller.title_font, bg="#2C3E50", fg="#ECF0F1",
            wraplength=800,  # Adjust this value for the desired wrapping width
            justify="center"  # Can also use "left" or "right" for different alignment
        )
        self.label.place(relx=0.5, rely=0.5, anchor='center')

        # Quit button in the bottom center
        quit_button = tk.Button(
            self, text="Quit", font=controller.button_font,
            command=self.quit,
            bg="#C0392B", fg="#ECF0F1", width=20, height=2,
            relief='flat', bd=0, activebackground="#A93226"
        )
        quit_button.place(relx=0.5, rely=0.8, anchor='center')

    def tkraise(self, *args, **kwargs):
        # Update the congrats message each time the page is raised
        self.update_congrats_message()
        self.play_completion_music()
        super().tkraise(*args, **kwargs)

    
    def update_congrats_message(self):
        # Get the user's name from the stored user data
        name = self.controller.user_data.get('name', 'Player')  # Default to 'Player' if no name is available
        # Update the congrats message with the user's name
        self.label.config(text=f"Congrats {name}! You have won a $20 grab voucher. An email will be sent out shortly 🎉")

    def play_completion_music(self):
        self.controller.stop_music()
        """Play completion music once all topics are completed."""
        if os.path.exists(self.controller.complete_sound_file):
            pygame.mixer.music.load(self.controller.complete_sound_file)
            pygame.mixer.music.play(-1)  # Loop Complete.mp3
            self.controller.current_music = self.controller.complete_sound_file


        
  

class Maths1Page(HangmanGamePage):
    def __init__(self, parent, controller):
        self.incorrect_attempts = 0 
        self.incorrect_guesses = set()
        questions_list = ['Implication is p → q, What is q → p', 'What is a set of distinct objects that is in an ordered arrangment', 'A compound proposition that is always true'] 
        words_list = ["converse", "permutation", "tautology"]  
        super().__init__(parent, controller, "Maths 1", words_list, questions_list)

class ProgrammingFundamentalsPage(HangmanGamePage):
    def __init__(self, parent, controller):
        self.incorrect_attempts = 0 
        self.incorrect_guesses = set()
        questions_list = ["What does tuple use","Value of object that can change","Comment that shows as first line of code"]   
        words_list = ['parentheses','mutable','docstring'] 
        super().__init__(parent, controller, "Programming Fundamentals", words_list, questions_list)

class IntroToComputingPage(HangmanGamePage):
    def __init__(self, parent, controller):
        self.incorrect_attempts = 0 
        self.incorrect_guesses = set()
        questions_list = ['Represent number up to base 16','Flip flop is a what kind of device','Boolean expression resulting in 1'] 
        words_list = ["hexadecimal","synchronous","minterm"]  
        super().__init__(parent, controller, "Intro to Computing", words_list, questions_list)

class ComputerOrganizationAndArchitecturePage(HangmanGamePage):
    def __init__(self, parent, controller):
        self.incorrect_attempts = 0 
        self.incorrect_guesses = set()
        questions_list = ['What memory that has very fast access but limited numbers within CPU','Two separate memory for code and data','What converts mnemonics in source file into machine code'] 
        words_list = ["registers","harvard","assembler"] 
        super().__init__(parent, controller, "Computer Org and Arch", words_list, questions_list)

if __name__ == "__main__":
    app = App()
    app.mainloop()
