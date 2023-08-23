### GEO UPLOADER SCRIPT FOR SINGLE-CELL DATASETS
### FGCZ
### WRITTEN FOR R 4.3.0.

library(tools)
################################################ 
### SET VARIABLES HERE
## RAW FILES

# Project number
fgcz_p = 24876

# SUSHI path after "Index of"
sushi_raw_path = "/projects/p24876/NovaSeq_20220906_NOV1425_o29380_DataDelivery"

## PROCESSED FILES

sushi_processed_path = "/projects/p24876/o29380_CellRangerCount_2022-09-08--17-47-41"

################################################ 
### PART 1: TSV GENERATION

# create directory for project upload
uploader_path = paste('/scratch/p',as.character(fgcz_p),'_geo_upload/', sep="")
dir.create(uploader_path)

# create directory for output
output_path = paste(uploader_path,toString(fgcz_p),'_output',sep="")
dir.create(output_path)

## RAW FILES

# obtain .tar files for md5sums from the SUSHI folder

data_path = paste('/srv/gstore',sushi_raw_path,'/', sep='')

paste(data_path,list.files(data_path, "*.tar"),sep='')

# names of raw data tar files, in order to later find the subfolders for processed files (barcodes, features, matrix)
raw_data_folders <- c()
md5sums_vector <- c()
files_for_sums <- c()

# loop through all copied .tar files, untar and calculate md5sum
for (i in c(1,length(list.files(uploader_path)))) {
  new_dir = paste(uploader_path, 
                  substr(list.files(data_path, "*tar"), 1, nchar(list.files(data_path, "*tar")[i])-4)[i],
                  '/', sep='')
  raw_data_folders <- append(raw_data_folders, substr(list.files(data_path, "*tar"), 1, nchar(list.files(data_path, "*tar")[i])-4))
  # untar files into geo uploader project subfolder in scratch
  untar(paste(data_path,list.files(data_path, "*tar"),sep='')[i], exdir = uploader_path)
  
  # save filenames in vector
  files_for_sums <- append(files_for_sums, list.files(new_dir))
  print("Retrieved files for md5sum calculation:")
  list.files(new_dir)
  
  # save md5sums in vector
  md5sums_vector <- append(md5sums_vector, md5sum(files = paste(new_dir, list.files(new_dir),sep='')))
  
  # remove directory containing fastq.gz files (don't waste space)
  unlink(new_dir, recursive = TRUE)
}

rawfile_md5sums <- data.frame("file name" = files_for_sums,"file checksum" = md5sums_vector)
write.table(rawfile_md5sums, file = paste(output_path,'rawfile_md5sums.tsv',sep='/'), sep = '\t')

## PROCESSED FILES - filtered

data_path = paste('/srv/gstore',sushi_processed_path,'/', sep='')

processed_data_paths <- paste(data_path, list.files(data_path, "[o*]"), sep = '')
md5sums_vector_proc_interim <- c()

for (i in c(1,length(processed_data_paths))) {
  # lists the names of files that should be md5sum'd from each dataset
  target_folder_filtered <- paste(processed_data_paths[i],'filtered_feature_bc_matrix',sep='/')
  files_to_md5sum <- list.files(target_folder_filtered)
  files_parent_dir <- list.files(data_path, "[o*]")[i]
  # full path to the files to be mdsummed, length should be same as that of files_to_md5sum
  target_files <- paste(target_folder_filtered,files_to_md5sum,sep='/')
  # copy file into geo uploader script folder and add parent folder to the name to prevent overwriting 
  file.copy(target_files, uploader_path)
  file.rename(from = paste(uploader_path, files_to_md5sum, sep=''), to = paste(uploader_path,files_parent_dir,'_',files_to_md5sum, sep=''))
  # append new names to the md5sums vector
  md5sums_vector_proc_interim <- append(md5sums_vector_proc_interim, paste(uploader_path,files_parent_dir,'_',files_to_md5sum, sep=''))
}

files_for_sums_proc <- c()
md5sums_vector_proc <- c()

for (filename in md5sums_vector_proc_interim) {
  R.utils::gunzip(filename)
  filename_gunzip <- substr(filename,start = 1,stop = nchar(filename)-3)
  files_for_sums_proc <- append(files_for_sums_proc, strsplit(filename_gunzip,'/')[[1]][4])
  md5sums_vector_proc <- append(md5sums_vector_proc,md5sum(filename_gunzip))
}

procfile_md5sums <- data.frame("file name" = files_for_sums_proc,"file checksum" = md5sums_vector_proc)
write.table(procfile_md5sums, file = paste(output_path,'procfile_md5sums.tsv',sep='/'), sep = '\t')
