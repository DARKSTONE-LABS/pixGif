import cv2
import tkinter as tk
from tkinter import filedialog, Label, Entry, messagebox
from PIL import Image, ImageStat

class VideoToPixelArtConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("pixGif")
        self.root.geometry("300x300")

        self.video_path = None
        self.pixel_art_gif_path = None
        self.pixel_size_var = tk.StringVar()
        self.pixel_size_var.set("10")  # Default pixel size
        self.duration_var = tk.StringVar()
        self.duration_var.set("100")  # Default duration in milliseconds

        # UI components
        self.label_file = Label(root, text="Select a video file:")
        self.label_file.pack()

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_video, bg="red", fg="black")
        self.browse_button.pack()

        self.label_pixel_size = Label(root, text="Pixel Size:")
        self.label_pixel_size.pack()

        self.entry_pixel_size = Entry(root, textvariable=self.pixel_size_var)
        self.entry_pixel_size.pack()

        self.label_duration = Label(root, text="Frame Duration (ms):")
        self.label_duration.pack()

        self.entry_duration = Entry(root, textvariable=self.duration_var)
        self.entry_duration.pack()

        self.convert_button = tk.Button(root, text="Convert", command=self.convert_video, bg="red", fg="black")
        self.convert_button.pack()

    def browse_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
        if self.video_path:
            self.label_file.config(text=f"Selected video: {self.video_path}")

    def convert_frame_to_pixel_art(self, frame):
        pixel_size = int(self.pixel_size_var.get())
        width, height = frame.size

        for x in range(0, width, pixel_size):
            for y in range(0, height, pixel_size):
                block = frame.crop((x, y, x + pixel_size, y + pixel_size))
                average_color = tuple(int(value) for value in ImageStat.Stat(block).mean)
                frame.paste(Image.new("RGB", (pixel_size, pixel_size), average_color), (x, y))

        return frame

    def convert_video(self):
        if not self.video_path:
            return

        try:
            pixel_size = int(self.pixel_size_var.get())
            duration = int(self.duration_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid integers.")
            return

        # Set your desired output path and filename
        self.pixel_art_gif_path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF Files", "*.gif")])

        # Open the video file
        cap = cv2.VideoCapture(self.video_path)

        pixel_art_frames = []

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Convert frame to pixel art
            pixel_art_frame = self.convert_frame_to_pixel_art(Image.fromarray(frame))

            # Append pixel art frame to the list
            pixel_art_frames.append(pixel_art_frame)

        # Save the list of frames as a GIF
        pixel_art_frames[0].save(
            self.pixel_art_gif_path,
            save_all=True,
            append_images=pixel_art_frames[1:],
            duration=duration,
            loop=0
        )

        cap.release()

        messagebox.showinfo("Conversion Complete", "Pixel Art GIF created successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToPixelArtConverter(root)
    root.mainloop()
