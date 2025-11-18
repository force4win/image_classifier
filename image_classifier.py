import customtkinter
import tkinter.filedialog
from PIL import Image, ImageTk
import os
import tkinter.messagebox as messagebox
import re

class ImageClassifierApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Clasificador de Imágenes")
        self.geometry("1200x800") # Increased size for horizontal layout

        self.image_files = []
        self.current_image_index = -1
        self.folder_path = None
        self.image_groups = {} # Dictionary to store image_path: group_name

        # Configure grid layout for the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3) # Left 3/4
        self.grid_columnconfigure(1, weight=1) # Right 1/4

        # Left Frame (Image Display and Navigation)
        self.left_frame = customtkinter.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.left_frame.grid_rowconfigure(0, weight=1) # Image row
        self.left_frame.grid_rowconfigure(1, weight=0) # Current group label row
        self.left_frame.grid_rowconfigure(2, weight=0) # Navigation frame row
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.displayed_image_label = customtkinter.CTkLabel(self.left_frame, text="")
        self.displayed_image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Current group display below image
        self.current_group_display_label = customtkinter.CTkLabel(self.left_frame, text="Grupo actual: Ninguno", font=customtkinter.CTkFont(size=14, weight="bold"))
        self.current_group_display_label.grid(row=1, column=0, pady=(5, 0)) # Placed below image

        self.navigation_frame = customtkinter.CTkFrame(self.left_frame)
        self.navigation_frame.grid(row=2, column=0, pady=10)

        self.prev_button = customtkinter.CTkButton(self.navigation_frame, text="Anterior", command=self.show_previous_image)
        self.prev_button.pack(side="left", padx=5)

        self.image_counter_label = customtkinter.CTkLabel(self.navigation_frame, text="0/0")
        self.image_counter_label.pack(side="left", padx=5)

        self.next_button = customtkinter.CTkButton(self.navigation_frame, text="Siguiente", command=self.show_next_image)
        self.next_button.pack(side="left", padx=5)

        # Right Frame (Controls)
        self.right_frame = customtkinter.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid_rowconfigure(0, weight=0) # Welcome label
        self.right_frame.grid_rowconfigure(1, weight=0) # Select folder button
        self.right_frame.grid_rowconfigure(2, weight=0) # Folder path label
        self.right_frame.grid_rowconfigure(3, weight=0) # Classification frame
        self.right_frame.grid_rowconfigure(4, weight=0) # Full rename radio
        self.right_frame.grid_rowconfigure(5, weight=0) # Suffix rename radio
        self.right_frame.grid_rowconfigure(6, weight=1) # Spacer
        self.right_frame.grid_rowconfigure(7, weight=0) # Rename button
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self.right_frame, text="¡Bienvenido al Clasificador de Imágenes!")
        self.label.grid(row=0, column=0, pady=20, padx=20)

        self.select_folder_button = customtkinter.CTkButton(self.right_frame, text="Seleccionar Carpeta", command=self.select_folder)
        self.select_folder_button.grid(row=1, column=0, pady=10)

        self.folder_path_label = customtkinter.CTkLabel(self.right_frame, text="Ninguna carpeta seleccionada")
        self.folder_path_label.grid(row=2, column=0, pady=5)

        self.classification_frame = customtkinter.CTkFrame(self.right_frame) # Reparented
        self.classification_frame.grid(row=3, column=0, pady=10, padx=10, sticky="ew")
        self.classification_frame.grid_columnconfigure(1, weight=1) # Make entry expand

        self.group_label = customtkinter.CTkLabel(self.classification_frame, text="Nombre del Grupo:")
        self.group_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.group_entry = customtkinter.CTkEntry(self.classification_frame) # Reparented
        self.group_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.assign_group_button = customtkinter.CTkButton(self.classification_frame, text="Asignar Grupo", command=self.assign_group) # Reparented
        self.assign_group_button.grid(row=1, column=0, columnspan=2, pady=5)

        # self.current_group_display_label = customtkinter.CTkLabel(self.classification_frame, text="Grupo actual: Ninguno") # Reparented
        # self.current_group_display_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Checkbox para opción de renombrado
        self.rename_option_var = customtkinter.StringVar(value="add_suffix") # Default to add suffix
        self.full_rename_radio = customtkinter.CTkRadioButton(self.right_frame, text="Renombrar completamente (Grupo_001.ext)",
                                                              variable=self.rename_option_var, value="full_rename")
        self.full_rename_radio.grid(row=4, column=0, pady=(10, 0), sticky="w")

        self.suffix_rename_radio = customtkinter.CTkRadioButton(self.right_frame, text="Añadir sufijo (Original_Grupo.ext)",
                                                                variable=self.rename_option_var, value="add_suffix")
        self.suffix_rename_radio.grid(row=5, column=0, pady=(0, 10), sticky="w") # Removed padx=20

        # Frame para los botones de grupos detectados
        self.detected_groups_frame = customtkinter.CTkScrollableFrame(self.right_frame, label_text="Grupos Detectados")
        self.detected_groups_frame.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")
        self.right_frame.grid_rowconfigure(6, weight=1) # Make this frame expand vertically

        self.rename_button = customtkinter.CTkButton(self.right_frame, text="Renombrar Imágenes", command=self.rename_images, fg_color="red") # Reparented
        self.rename_button.grid(row=8, column=0, pady=20)

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

    def assign_group(self):
        if self.image_files and 0 <= self.current_image_index < len(self.image_files):
            current_image_path = self.image_files[self.current_image_index]
            group_name = self.group_entry.get().strip()
            if group_name:
                self.image_groups[current_image_path] = group_name
                self.current_group_display_label.configure(text=f"Grupo actual: {group_name}")
                print(f"Imagen '{os.path.basename(current_image_path)}' asignada al grupo '{group_name}'")
            else:
                if current_image_path in self.image_groups:
                    del self.image_groups[current_image_path]
                self.current_group_display_label.configure(text="Grupo actual: Ninguno")
                print(f"Grupo desasignado para la imagen '{os.path.basename(current_image_path)}'")
            
            # After assigning/unassigning, refresh the group buttons
            unique_groups_with_images = {} # {group_name: first_image_path}
            for img_path in self.image_files:
                g_name = self.image_groups.get(img_path)
                if g_name and g_name not in unique_groups_with_images:
                    unique_groups_with_images[g_name] = img_path
            sorted_unique_groups_with_images = {k: unique_groups_with_images[k] for k in sorted(unique_groups_with_images)}
            self.create_group_buttons(sorted_unique_groups_with_images)
        else:
            print("No hay imagen seleccionada para asignar grupo.")

    def load_images_from_folder(self):
        self.image_files = []
        self.image_groups = {} # Clear existing groups when loading a new folder
        if self.folder_path:
            for filename in os.listdir(self.folder_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    full_path = os.path.join(self.folder_path, filename)
                    self.image_files.append(full_path)
                    
                    # Attempt to parse group name from filename
                    group_name = None
                    base_name = os.path.splitext(filename)[0] # Get filename without extension
                    
                    # Prioritize add_suffix pattern: OriginalName_GroupName.ext
                    # Look for _GroupName at the very end of the base_name
                    match_suffix = re.search(r"_([A-Za-z0-9\s-]+)$", base_name, re.IGNORECASE) # More flexible regex
                    if match_suffix:
                        potential_group = match_suffix.group(1)
                        # Ensure the captured group name is not just a number
                        if not potential_group.isdigit():
                            group_name = potential_group
                    
                    # If no suffix group found, try full_rename pattern: GroupName_001.ext
                    if not group_name:
                        match_full = re.search(r"(.+?)_(\d{3})$", base_name, re.IGNORECASE) # Capture group name
                        if match_full:
                            group_name = match_full.group(1) # Extract the group name
                    
                    if group_name:
                        self.image_groups[full_path] = group_name
        
        self.image_files.sort() # Sort images for consistent order
        self.current_image_index = -1
        
        # Collect unique group names and their first image for buttons
        unique_groups_with_images = {} # {group_name: first_image_path}
        for img_path in self.image_files:
            group_name = self.image_groups.get(img_path)
            if group_name and group_name not in unique_groups_with_images:
                unique_groups_with_images[group_name] = img_path
        
        # Sort groups by name
        sorted_unique_groups_with_images = {k: unique_groups_with_images[k] for k in sorted(unique_groups_with_images)}
        
        self.create_group_buttons(sorted_unique_groups_with_images)

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
                
                # Ensure layout is updated before querying dimensions
                self.left_frame.update_idletasks()
                
                # Resize image to fit within the frame, maintaining aspect ratio
                max_width = self.left_frame.winfo_width() - 20 # Subtract padding
                max_height = self.left_frame.winfo_height() - 20 # Subtract padding

                if max_width <= 0 or max_height <= 0: # Handle initial state where frame size might be 0
                    max_width = 700
                    max_height = 500

                pil_image.thumbnail((max_width, max_height), Image.LANCZOS)
                
                ctk_image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=(pil_image.width, pil_image.height))
                self.displayed_image_label.configure(image=ctk_image, text="")
                self.image_counter_label.configure(text=f"{self.current_image_index + 1}/{len(self.image_files)}")
                
                # Update group display
                current_image_path = self.image_files[self.current_image_index]
                assigned_group = self.image_groups.get(current_image_path, "Ninguno")
                self.current_group_display_label.configure(text=f"Grupo actual: {assigned_group}")
                self.group_entry.delete(0, "end")
                if assigned_group != "Ninguno":
                    self.group_entry.insert(0, assigned_group)

            except Exception as e:
                self.displayed_image_label.configure(image=None, text=f"Error al cargar la imagen: {e}")
                self.image_counter_label.configure(text="0/0")
                self.current_group_display_label.configure(text="Grupo actual: Ninguno")
                self.group_entry.delete(0, "end")
        else:
            self.displayed_image_label.configure(image=None, text="No hay imágenes para mostrar.")
            self.image_counter_label.configure(text="0/0")
            self.current_group_display_label.configure(text="Grupo actual: Ninguno")
            self.group_entry.delete(0, "end")

    def show_next_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.display_image()

    def show_previous_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index - 1 + len(self.image_files)) % len(self.image_files)
            self.display_image()

    def rename_images(self):
        if not self.image_groups:
            messagebox.showinfo("Renombrar Imágenes", "No hay imágenes asignadas a ningún grupo para renombrar.")
            return

        confirmation = messagebox.askyesno("Confirmar Renombrado", 
                                                        "¿Estás seguro de que quieres renombrar las imágenes? Esta acción no se puede deshacer.")
        if not confirmation:
            return

        renamed_count = 0
        errors = []
        
        rename_mode = self.rename_option_var.get()

        # Group images by their assigned group name
        grouped_images = {}
        for img_path, group_name in self.image_groups.items():
            if group_name not in grouped_images:
                grouped_images[group_name] = []
            grouped_images[group_name].append(img_path)

        for group_name, image_paths in grouped_images.items():
            counter = 1
            for old_path in image_paths:
                directory, filename = os.path.split(old_path)
                name, ext = os.path.splitext(filename)
                
                new_name_base = ""
                if rename_mode == "full_rename":
                    new_name_base = f"{group_name}_{counter:03d}"
                elif rename_mode == "add_suffix":
                    # Remove any existing group_XXX suffix if present from previous renames
                    original_name_match = re.match(r"(.+?)(?:_[A-Za-z0-9]+_\d{3})?$", name) # Adjusted regex to be more flexible for existing suffixes
                    if original_name_match:
                        original_base_name = original_name_match.group(1)
                    else:
                        original_base_name = name # Fallback if no pattern match

                    new_name_base = f"{original_base_name}_{group_name}"
                    # If multiple files with same original name get same group, add counter
                    # This part needs careful consideration to avoid clashes.
                    # For simplicity, let's just add the counter for uniqueness if needed.
                    
                new_name = f"{new_name_base}{ext}"
                new_path = os.path.join(directory, new_name)

                try:
                    # Ensure the new name doesn't clash with an existing file that's not being renamed
                    temp_counter = 1
                    final_new_name = new_name
                    final_new_path = new_path

                    while os.path.exists(final_new_path) and final_new_path != old_path:
                        if rename_mode == "full_rename":
                            final_new_name = f"{group_name}_{counter:03d}_{temp_counter:02d}{ext}" # Add extra counter for clash
                        elif rename_mode == "add_suffix":
                            final_new_name = f"{new_name_base}_{temp_counter:02d}{ext}" # Add extra counter for clash
                        
                        final_new_path = os.path.join(directory, final_new_name)
                        temp_counter += 1
                    
                    if temp_counter > 1:
                        print(f"Advertencia: '{new_name}' ya existía, usando '{final_new_name}' en su lugar.")

                    os.rename(old_path, final_new_path)
                    renamed_count += 1
                    print(f"Renombrado: '{old_path}' a '{final_new_path}'")
                except OSError as e:
                    errors.append(f"Error al renombrar '{os.path.basename(old_path)}' a '{os.path.basename(final_new_path)}': {e}")
                counter += 1
        
        if errors:
            error_message = "Se encontraron los siguientes errores al renombrar:\n" + "\n".join(errors)
            messagebox.showerror("Errores al Renombrar", error_message)
        
        messagebox.showinfo("Renombrado Completado", 
                                        f"Se renombraron {renamed_count} imágenes. {len(errors)} errores.")
        
        # Clear groups and reload images to reflect changes
        self.image_groups = {}
        self.load_images_from_folder() # Reload images from the current folder

    def create_group_buttons(self, unique_groups_with_images):
        # Clear existing buttons
        for widget in self.detected_groups_frame.winfo_children():
            widget.destroy()
        
        # Configure grid for the scrollable frame
        self.detected_groups_frame.grid_columnconfigure((0, 1, 2), weight=1) # 3 columns, equally weighted

        if not unique_groups_with_images:
            label = customtkinter.CTkLabel(self.detected_groups_frame, text="No hay grupos detectados.")
            label.grid(row=0, column=0, columnspan=3, pady=5, padx=5)
            return

        button_image_size = (60, 60) # Fixed square size for button images
        row_idx = 0
        col_idx = 0
        max_cols = 3

        for group_name, image_path in unique_groups_with_images.items():
            try:
                pil_image = Image.open(image_path)
                pil_image.thumbnail(button_image_size, Image.LANCZOS)
                ctk_image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=button_image_size)
                
                button = customtkinter.CTkButton(self.detected_groups_frame, text=group_name, 
                                                 image=ctk_image, compound="top", # Changed to "top"
                                                 command=lambda g=group_name: self.assign_group_from_button(g))
                button.grid(row=row_idx, column=col_idx, pady=2, padx=2, sticky="ew")
            except Exception as e:
                print(f"Error al cargar la imagen para el botón del grupo '{group_name}': {e}")
                # Fallback to text-only button if image fails to load
                button = customtkinter.CTkButton(self.detected_groups_frame, text=group_name, 
                                                 command=lambda g=group_name: self.assign_group_from_button(g))
                button.grid(row=row_idx, column=col_idx, pady=2, padx=2, sticky="ew")
            
            col_idx += 1
            if col_idx >= max_cols:
                col_idx = 0
                row_idx += 1

    def assign_group_from_button(self, group_name):
        self.group_entry.delete(0, "end")
        self.group_entry.insert(0, group_name)
        self.assign_group() # Call the existing assign_group method

if __name__ == "__main__":
    app = ImageClassifierApp()
    app.mainloop()
