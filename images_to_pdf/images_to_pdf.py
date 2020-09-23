import os
import img2pdf

from .settings import settings

class ImagesToPdf():

  EXTENSION_PDF = ".pdf"
  OUTPUT_SUB_DIR = "output"
  FILE_TYPES = ["jpg", "JPG", "png", "PNG"]

  def __init__(self):
    self.target_dir = settings.TARGET_DIR
    pass

  def exec(self):
    dir_file_list = os.listdir(self.target_dir)
    dir_list = [d for d in dir_file_list if os.path.isdir(os.path.join(self.target_dir, d))]
    for d in dir_list:
      input_dir = os.path.join(self.target_dir, d)
      self.convert(input_dir)


  def convert(self, input_dir):
    dir_file_list = os.listdir(input_dir)
    input_files = [f for f in dir_file_list if self.check_file_type(input_dir, f)]

    if len(input_files) <= 0:
      print("There are not target file in this directory.：" + input_dir)
      return
    input_files.sort()

    output_dir = os.path.join(input_dir, self.OUTPUT_SUB_DIR)
    os.makedirs(output_dir, exist_ok=True)
    file_name = self.create_file_name(input_dir)
    output_file_path = os.path.join(output_dir, file_name)
    if os.path.exists(output_file_path):
      os.remove(output_file_path)

    with open(output_file_path, "wb") as pdf:
      pdf.write(img2pdf.convert(self.join_path(input_dir, input_files)))

    return

  def create_file_name(self, input_dir):
    filename = os.path.basename(input_dir) + self.EXTENSION_PDF
    return filename

  def check_file_type(self, input_dir, target_file):
    file_path = os.path.join(os.path.join(input_dir, target_file))
    if not os.path.isfile(file_path):
      return False
    for file_type in self.FILE_TYPES:
      if file_path.endswith(file_type):
        return True

    return False

  def join_path(self, input_dir, tmp_input_files):
    input_files = []
    for input_file in tmp_input_files:
      input_files.append(os.path.join(input_dir, input_file))

    return input_files