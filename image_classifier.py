import customtkinter
import tkinter.filedialog
from PIL import Image, ImageTk
import os

class ImageClassifierApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Clasificador de Imágenes")
        self.geometry("1000x800") # Increased size for image display

        self.image_files = []
        self.current_image_index = -1
        self.folder_path = None

        # Frame para la imagen y los controles
        self.image_frame = customtkinter.CTkFrame(self)
        self.image_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.displayed_image_label = customtkinter.CTkLabel(self.image_frame, text="")
        self.displayed_image_label.pack(pady=10, padx=10, fill="both", expand=True)

        # Etiqueta de bienvenida
        self.label = customtkinter.CTkLabel(self, text="¡Bienvenido al Clasificador de Imágenes!")
        self.label.pack(pady=20, padx=20)

        # Botón para seleccionar carpeta
        self.select_folder_button = customtkinter.CTkButton(self, text="Seleccionar Carpeta", command=self.select_folder)
        self.select_folder_button.pack(pady=10)

        # Etiqueta para mostrar la carpeta seleccionada
        self.folder_path_label = customtkinter.CTkLabel(self, text="Ninguna carpeta seleccionada")
        self.folder_path_label.pack(pady=5)

        # Controles de navegación de imágenes
        self.navigation_frame = customtkinter.CTkFrame(self)
        self.navigation_frame.pack(pady=10)

        self.prev_button = customtkinter.CTkButton(self.navigation_frame, text="Anterior", command=self.show_previous_image)
        self.prev_button.pack(side="left", padx=5)

        self.image_counter_label = customtkinter.CTkLabel(self.navigation_frame, text="0/0")
        self.image_counter_label.pack(side="left", padx=5)

        self.next_button = customtkinter.CTkButton(self.navigation_frame, text="Siguiente", command=self.show_next_image)
        self.next_button.pack(side="left", padx=5)

    def select_folder(self):
        folder_path = tkinter.filedialog.askdirectory()
        if folder_path:
            self.folder_path = folder_path
            self.folder_path_label.configure(text=f"Carpeta seleccionada: {folder_path}")
            print(f"Carpeta seleccionada: {folder_path}")
            self.load_images_from_folder()
        else:
            self.folder_path_label.configure(text="Selección de carpeta cancelada")
            print("Selección de carpeta cancelada")

    def load_images_from_folder(self):
        self.image_files = []
        if self.folder_path:
            for filename in os.listdir(self.folder_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    self.image_files.append(os.path.join(self.folder_path, filename))
        
        self.image_files.sort() # Sort images for consistent order
        self.current_image_index = -1
        if self.image_files:
            self.current_image_index = 0
            self.display_image()
        else:
            self.displayed_image_label.configure(image=None)
            self.displayed_image_label.configure(text="No se encontraron imágenes en esta carpeta.")
            self.image_counter_label.configure(text="0/0")

    def display_image(self):
        if self.image_files and 0 <= self.current_image_index < len(self.image_files):
            image_path = self.image_files[self.current_image_index]
            try:
                pil_image = Image.open(image_path)
                
                # Resize image to fit within the frame, maintaining aspect ratio
                max_width = self.image_frame.winfo_width() - 20 # Subtract padding
                max_height = self.image_frame.winfo_height() - 20 # Subtract padding

                if max_width <= 0 or max_height <= 0: # Handle initial state where frame size might be 0
                    max_width = 700
                    max_height = 500

                pil_image.thumbnail((max_width, max_height), Image.LANCZOS)
                
                ctk_image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=(pil_image.width, pil_image.height))
                self.displayed_image_label.configure(image=ctk_image, text="")
                self.image_counter_label.configure(text=f"{self.current_image_index + 1}/{len(self.image_files)}")
            except Exception as e:
                self.displayed_image_label.configure(image=None, text=f"Error al cargar la imagen: {e}")
                self.image_counter_label.configure(text="0/0")
        else:
            self.displayed_image_label.configure(image=None, text="No hay imágenes para mostrar.")
            self.image_counter_label.configure(text="0/0")

    def show_next_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.display_image()

    def show_previous_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index - 1 + len(self.image_files)) % len(self.image_files)
            self.display_image()

if __name__ == "__main__":
    app = ImageClassifierApp()
    app.mainloop()
