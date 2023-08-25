### GEO UPLOADER SCRIPT FOR SINGLE-CELL DATASETS
### FGCZ
### WRITTEN FOR R 4.3.0.

library(tools)
library(ezRun)
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
uploader_path = paste('/scratch/p',as.character(fgcz_p),'_geo_upload', sep="")
dir.create(uploader_path)

# create directory for output
output_path = paste0(uploader_path,'/',toString(fgcz_p),'_output')
dir.create(output_path)

## RAW FILES

dataset <- ezRead.table(paste0("/srv/gstore", sushi_raw_path, "/dataset.tsv"))
tarFiles <- paste0("/srv/gstore/projects/", dataset$`RawDataDir [File]`)

# obtain .tar files for md5sums from the SUSHI folder
cmd <- paste('cp', paste(tarFiles, collapse = " "), output_path)
system(cmd)

# names of raw data tar files, in order to later find the subfolders for processed files (barcodes, features, matrix)
md5sums <- list()

# loop through all copied .tar files, untar and calculate md5sum
for (myTarFile in tarFiles) {
  new_dir = paste0(uploader_path, "/", sub(".tar$", "",
                                           basename(myTarFile)))
  # untar files into geo uploader project subfolder in scratch
  # untar(myTarFile, exdir = uploader_path)
  md5sums[[myTarFile]] <- md5sum(files = list.files(new_dir, full.names
                                                    = TRUE))
}

rawfile_md5sums <- data.frame("file name" = basename(unlist(lapply(md5sums, names))),
                              "file checksum" = unlist(md5sums,
                                                       use.names = FALSE), row.names = NULL, check.names = FALSE)

writexl::write_xlsx(x = rawfile_md5sums, path = paste(output_path,'rawfile_md5sums.xlsx', sep='/'))

## PROCESSED (filtered barcodes, features, matrix)

dataset_proc <- ezRead.table(paste0("/srv/gstore", sushi_processed_path, "/dataset.tsv"))
proc_paths <- paste0("/srv/gstore/projects/", dataset_proc$`CountMatrix [Link]`)

cmd <- paste('cp -r', paste(proc_paths, collapse = " "), output_path)
system(cmd)

md5sums_proc <- list()
md5sums[[myTarFile]] <- md5sum(files = list.files(new_dir, full.names
                                                  = TRUE))

for (i in seq_along(rownames(dataset_proc))) {
  
  # create new folders to put filtered processed files without overwriting folder
  dataset_name <- rownames(dataset_proc)[i]
  new_dir <- paste0(output_path,'/filtered_', dataset_name)
  print(new_dir)

  cmd <- paste0('cp -r ', proc_paths[i],' ', new_dir)
  system(cmd)
  
  # put renamed files into the output folder, remove subfolders
  print(list.files(new_dir))
  file.rename(from = paste(new_dir, list.files(new_dir), sep='/'), to = paste0(output_path,'/',dataset_name,'_',list.files(new_dir)))
  unlink(new_dir, recursive = TRUE)
  
  new_proc_files <- list.files(output_path, '*gz', full.names = TRUE)
  
  for (filename in new_proc_files) {
    R.utils::gunzip(filename)
  }
  
  md5sums_proc[[dataset_name]] <- md5sum(files = sub(".gz$", "", new_proc_files))
}

cmd <- paste('rm -r', paste0(output_path,'/','filtered_feature_bc_matrix'))
system(cmd)

procfile_md5sums <- data.frame("file name" = basename(unlist(lapply(md5sums_proc, names))),
                              "file checksum" = unlist(md5sums_proc,
                                                       use.names = FALSE), row.names = NULL, check.names = FALSE)

writexl::write_xlsx(x = procfile_md5sums, path = paste(output_path,'procfile_md5sums.xlsx', sep='/'))
