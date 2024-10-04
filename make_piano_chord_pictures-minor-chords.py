from PIL import Image
import os

# Load the image
image_path = 'pictures/minor_chords-crop.jpg'
image = Image.open(image_path)

# Dimensions of the original image
width, height = image.size


# Dimensions of each chord box
columns = 3  # Root Position, 1st Inversion, 2nd Inversion
rows = 12    # Number of chords

# Define the width and height for each section
box_width = width // columns
box_height = height // rows

# Names of the chords in order
chord_names = [
   "C_Minor", "C#_Db_Minor", "D_Minor", "D#_Eb_Minor", "E_Minor",
   "F_Minor", "F#_Gb_Minor", "G_Minor", "G#_Ab_Minor", "A_Minor",
   "A#_Bb_Minor", "B_Minor"
]

# Corresponding positions
positions = ["Root_Position", "1st_Inversion", "2nd_Inversion"]

# Prepare output directory
output_dir = 'output/Minor_triads_chords'
os.makedirs(output_dir, exist_ok=True)

# Loop through each chord and inversion, and save the corresponding image segment
for row in range(rows):
   for col in range(columns):
      # Calculate box boundaries
      left = col * box_width
      upper = row * box_height
      right = left + box_width
      lower = upper + box_height

      # Crop the image
      cropped_image = image.crop((left, upper, right, lower))

      # Generate the filename
      chord_name = chord_names[row]
      position = positions[col]
      output_filename = f"{chord_name}_{position}.png"
      output_path = os.path.join(output_dir, output_filename)

      # Save the cropped image
      cropped_image.save(output_path)
