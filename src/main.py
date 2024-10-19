from DVD import *
import cv2
import numpy as np
import datetime
import os

# Obtener la fecha actual para el nombre del archivo
current_day = datetime.datetime.now().strftime("%Y%m%d")

# Definir el directorio donde deseas guardar el video
output_directory = "./videos/"  # Asegurate de que este directorio exista

# Crear el nombre del archivo incluyendo la fecha
output_filename = f"dvd_screener_{current_day}.mp4"

# Combinar la ruta y el nombre del archivo
output_path = os.path.join(output_directory, output_filename)

#Configuracion para grabar video con OpenCV
fps = 60
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codificador para mp4

# Guardar el video
output_video = cv2.VideoWriter(output_path, fourcc, fps, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Tiempo maximo de grabacion en segundos
max_duration = 20

def main():
    pg.init()
    
    window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Pygame - Bouncing DVD logo")
    
    dvd = DVD(window)
    pg.display.set_icon(dvd.logo)
    
    # 1 for foreground color change (default), 2 for background color change
    option = 2
    if option == 2:
        dvd.logo = pg.transform.smoothscale(dvd.sprite, (dvd.width, dvd.height)) 
        dvd.color = (0, 0, 0, 0)
        
    clock = pg.time.Clock()

    # Variable para contar fotogramas
    frame_count = 0
    
    running = True
    while running:
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                running = False

        window.fill('#101010')
        
        dvd.update()
        dvd.render()
        
        clock.tick(fps)
        pg.display.flip()

        # Capturar el fotograma de la ventana
        frame = pg.surfarray.array3d(window)
        frame = np.transpose(frame, (1, 0, 2)) 
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convertir de RGB a BGR para OpenCV

        # Escribir el fotograma en el archivo de video
        output_video.write(frame)

        # Incrementa el contador de fotogramas
        frame_count += 1

        # Verificar si ha pasado el tiempo maximo
        #if time.time() - start_time > max_duration:
        #    running = False

        if frame_count > max_duration * fps:
            running = False

        print(frame_count)

if __name__ == '__main__':
    main()
