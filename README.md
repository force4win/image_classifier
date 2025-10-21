# Clasificador de Imágenes

Una aplicación de escritorio simple para clasificar y renombrar imágenes por grupos.

## Características

-   **Selección de Carpeta:** Permite al usuario seleccionar una carpeta que contenga imágenes.
-   **Visualización de Imágenes:** Muestra las imágenes una a una con botones de navegación.
-   **Clasificación por Grupos:** Permite asignar un nombre de grupo a cada imagen.
-   **Renombrado de Archivos:** Renombra las imágenes basándose en el grupo asignado, añadiendo un número secuencial (ej. `NombreGrupo_001.jpg`).

## Requisitos

-   Python 3.x
-   Librerías Python: `customtkinter`, `Pillow`

## Instalación

1.  **Clonar el repositorio (o descargar los archivos):**

    ```bash
    git clone <URL_DEL_REPOSITORIO> # Si está en un repositorio
    cd CLASIFICADOR_IMAGENES
    ```

2.  **Instalar las librerías necesarias:**

    Abre tu terminal o línea de comandos y ejecuta:

    ```bash
    pip install customtkinter Pillow
    ```

## Cómo Ejecutar

1.  Navega al directorio del proyecto en tu terminal:

    ```bash
    cd D:\WORKSPACE\WORKSPACE_PORTFOLIO\CLASIFICADOR_IMAGENES
    ```

2.  Ejecuta el script principal:

    ```bash
    python image_classifier.py
    ```

## Uso

1.  **Seleccionar Carpeta:** Haz clic en el botón "Seleccionar Carpeta" y elige el directorio que contiene tus imágenes.
2.  **Navegar Imágenes:** Usa los botones "Anterior" y "Siguiente" para moverte entre las imágenes.
3.  **Asignar Grupo:** Para cada imagen, escribe un nombre de grupo en el campo de texto y haz clic en "Asignar Grupo". El grupo asignado se mostrará junto a la imagen.
4.  **Renombrar Imágenes:** Una vez que hayas asignado grupos a tus imágenes, haz clic en el botón "Renombrar Imágenes". La aplicación te pedirá confirmación antes de proceder.

## Advertencia Importante

La función de renombrado de archivos **modificará permanentemente los nombres de tus imágenes**. Se recomienda encarecidamente que pruebes esta funcionalidad con una **copia de tus imágenes** o en una carpeta con imágenes de prueba para evitar la pérdida o modificación no deseada de tus archivos originales.
