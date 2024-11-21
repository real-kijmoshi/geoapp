import numpy as np
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0.6, 0.8, 1)  # Vibrant blue
        self.color = (1, 1, 1, 1)  # White text
        self.bold = True
        self.size_hint_y = None
        self.height = dp(50)
        self.background_normal = ''
        self.background_down = ''

class FileProcessingApp(App):
    def build(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # Title Label
        title_label = Label(
            text='File Processing Utility', 
            font_size=dp(24), 
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None, 
            height=dp(50)
        )
        main_layout.add_widget(title_label)

        # Status Label
        self.status_label = Label(
            text='Choose a file to process', 
            color=(0.4, 0.4, 0.4, 1),
            size_hint_y=None, 
            height=dp(40)
        )
        main_layout.add_widget(self.status_label)

        # File Chooser
        self.file_chooser = FileChooserListView(
            filters=['*.txt'],  # Limit to text-based files
            size_hint=(1, 0.5)
        )
        main_layout.add_widget(self.file_chooser)

        # Scrollable Output Box
        scroll_view = ScrollView(size_hint=(1, 0.3))
        self.output_box = TextInput(
            text='', 
            readonly=True, 
            multiline=True,
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        scroll_view.add_widget(self.output_box)
        main_layout.add_widget(scroll_view)

        # Button Layout
        button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        # Upload Button
        upload_btn = StyledButton(text='Upload & Process')
        upload_btn.bind(on_press=self.upload_and_process)
        button_layout.add_widget(upload_btn)

        # Download Button
        download_btn = StyledButton(text='Download Processed')
        download_btn.bind(on_press=self.download_file)
        button_layout.add_widget(download_btn)

        main_layout.add_widget(button_layout)

        return main_layout

    def upload_and_process(self, instance):
        selected = self.file_chooser.selection
        if selected:
            file_path = selected[0]
            try:
                print(f"Processing file: {file_path}")
                # Read points from the file
                points = np.array([
                    np.array(line.split(" ")[1:], dtype=np.float64)
                    for line in open(file_path).readlines()
                ])

                # Build matrices
                tmp_A = [[*point[0:2], 1] for point in points]
                A = np.matrix(tmp_A)
                B = np.matrix(points[:, 2]).T

                # Perform computation
                fit = (A.T * A).I * A.T * B

                # Display results
                results = f"Fit Results:\n{fit}\n\n"
                results += f"B Matrix Size: {B.size}\nA Matrix Size: {A.size}"
                print(results)
                self.processed_content = results
                self.output_box.text = results
                self.status_label.text = f"Processed: {os.path.basename(file_path)}"
            except Exception as e:
                self.status_label.text = f"Error processing file: {str(e)}"
                self.output_box.text = ''
        else:
            self.status_label.text = "No file selected. Please choose a file."

    def download_file(self, instance):
        if hasattr(self, 'processed_content'):
            try:
                # Create a dedicated downloads folder if it doesn't exist
                download_dir = os.path.join(os.path.expanduser('~'), 'Downloads', 'FileProcessing')
                os.makedirs(download_dir, exist_ok=True)
                
                output_path = os.path.join(download_dir, 'processed_file.txt')
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(self.processed_content)
                
                self.status_label.text = f"File saved: {output_path}"
            except Exception as e:
                self.status_label.text = f"Download failed: {str(e)}"
        else:
            self.status_label.text = "No file processed. Upload a file first."

if __name__ == '__main__':
    FileProcessingApp().run()
