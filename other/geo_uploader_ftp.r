### GEO UPLOADER SCRIPT FOR SINGLE-CELL DATASETS
### PART 2 - FTP UPLOAD
### FGCZ
### WRITTEN FOR R 4.3.0.

library(tools)
library(ezRun)

################################################ 
### SET VARIABLES HERE

## METADATA FILE

file_dir = '/scratch/p24876_geo_upload/24876_output'
metadata_file = '/scratch/p24876_geo_upload/24876_output/infolist.xlsx'
upload_space = 'uploads/insert-user'
username = ''
password = ''
host_address = 'ftp-private.ncbi.nlm.nih.gov'

################################################ 
### PART 1: CHECK IF FILES PRESENT AND IDENTICAL

print("Reading the metadata sheet...")

if (file.exists(metadata_file)){
  metadata_df <- readxl::read_excel(metadata_file, sheet = 3)
  procfile_md5sums <- readxl::read_excel(metadata_file, sheet = 3)
  rawfile_md5sums <- readxl::read_excel(metadata_file, sheet = 2)
} else {
  print("Provided metadata sheet not found. Searching for file basename in provided folder...")
  if (file.exists(paste(file_dir, basename(metadata_file), sep='/'))) {
    print('Found a metadata sheet. Reading...')
    metadata_file <- paste(file_dir, basename(metadata_file), sep='/')
    metadata_df <- readxl::read_excel(metadata_file, sheet = 1)
    procfile_md5sums <- readxl::read_excel(metadata_file, sheet = 3)
    rawfile_md5sums <- readxl::read_excel(metadata_file, sheet = 2)
  } else {
    print("No metadata file found. Exiting the script...")
  }
  }

metadata_df <- readxl::read_excel(metadata_file, sheet = 1)
procfile_md5sums <- readxl::read_excel(metadata_file, sheet = 3)
rawfile_md5sums <- readxl::read_excel(metadata_file, sheet = 2)

print("Metadata, Rawfile and Processed file information obtained.")
print("Checking if all raw files are present and md5sums identical for upload...")

proceed_with_transfer = TRUE

for (filename in rawfile_md5sums$`file name`) {
  searched_file <- paste(file_dir, filename, sep = '/')
  if (file.exists(searched_file) == FALSE) {
    print(paste(filename, 'does not exist in the provided directory!'))
    proceed_with_transfer = FALSE
  }
  if (file.exists(searched_file) == TRUE) {
    md5sum_of_searched_file = md5sum(searched_file)
    real_md5sum = rawfile_md5sums$`file checksum`[rawfile_md5sums$`file name` == filename]
    if (md5sum_of_searched_file != real_md5sum) {
      print(paste(filename, 'expected md5sums do not match with md5sums of file in the provided dictionary!'))
      proceed_with_transfer = FALSE
    }
  }
}

for (filename in procfile_md5sums$`file name`) {
  searched_file <- paste(file_dir, filename, sep = '/')
  if (file.exists(searched_file) == FALSE) {
    print(paste(filename, 'does not exist in the provided directory!'))
    proceed_with_transfer = FALSE
  }
  if (file.exists(searched_file) == TRUE) {
    md5sum_of_searched_file = md5sum(searched_file)
    real_md5sum = procfile_md5sums$`file checksum`[procfile_md5sums$`file name` == filename]
    if (md5sum_of_searched_file != real_md5sum) {
      print(paste(filename, 'expected md5sums do not match with md5sums of file in the provided dictionary!'))
      proceed_with_transfer = FALSE
    }
  }
}

if (proceed_with_transfer == TRUE) {
  print("Proceeding with file transfer to GEO database...")
} else {
  print("Please make sure you have the right metadata sheet and all its mentioned files in the provided data folder!")
}
################################################ 
### PART 1: TRANSFER FILES TO GEO

print("Starting file transfer to GEO server...")

base_command <- paste('ncftpput -u',username,'-p',password, host_address, upload_space)

print("Uploading metadata sheet...")
cmd <- paste(base_command, metadata_file)
system(cmd)

print("Uploading raw files...")

for (filename in rawfile_md5sums$`file name`) {
  print(paste("Uploading", filename,"..."))
  searched_file <- paste(file_dir, filename, sep = '/')
  cmd <- paste(base_command, searched_file)
  system(cmd)
  }

print("Uploading processed files...")

for (filename in procfile_md5sums$`file name`) {
  print(paste("Uploading", filename,"..."))
  searched_file <- paste(file_dir, filename, sep = '/')
  cmd <- paste(base_command, searched_file)
  system(cmd)
  }

print("Upload complete.")


