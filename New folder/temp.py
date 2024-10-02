import tempfile

# Get the location of the temp directory
temp_dir = tempfile.gettempdir()

print(f"The temporary file directory is: {temp_dir}")
