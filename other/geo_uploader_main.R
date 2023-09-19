### GEO UPLOADER SCRIPT FOR SINGLE-CELL DATASETS
### PART 1 - METADATA CREATION
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
### PART 1: XLSX GENERATION

# define output for metadata and info sheet

infolist <- list()

file_metadata <- list()


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
  tar_name <- sub(".tar$", "",
                  basename(myTarFile))
  # start adding information to the first sheet for sample metadata
  file_metadata[[tar_name]] <- c("library name" = tar_name, "title" = tar_name, "organism" = dataset[tar_name, "Species"], 
                                 "tissue" = '', "cell line" = '', "cell type" = '', "genotype" = '', "treatment" = '',
                                 "molecule"= '', "single or paired-end"	= '', "instrument model" = '',	"description" = '')
  
  new_dir = paste0(uploader_path, "/", tar_name)
  # untar files into geo uploader project subfolder in scratch
  untar(myTarFile, exdir = output_path)
  md5sums[[myTarFile]] <- md5sum(files = list.files(new_dir, full.names
                                                    = TRUE))
  rawfiles_for_metadata <- c("raw file" = basename(names(md5sums[[myTarFile]])))


  file_metadata[[tar_name]] <- append(file_metadata[[tar_name]], rawfiles_for_metadata)
  
}

rawfile_md5sums <- data.frame("file name" = basename(unlist(lapply(md5sums, names))),
                              "file checksum" = unlist(md5sums,
                                                       use.names = FALSE), row.names = NULL, check.names = FALSE)

## PROCESSED (filtered barcodes, features, matrix)

dataset_proc <- ezRead.table(paste0("/srv/gstore", sushi_processed_path, "/dataset.tsv"))
proc_paths <- paste0("/srv/gstore/projects/", dataset_proc$`CountMatrix [Link]`)

cmd <- paste('cp -r', paste(proc_paths, collapse = " "), output_path)
system(cmd)

md5sums_proc <- list()

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
  
  new_proc_filenames <- c("processed data file" = basename(sub(".gz$", "", new_proc_files)))
  md5sums_proc[[dataset_name]] <- md5sum(files = new_proc_filenames)

  file_metadata[[dataset_name]] <- append(file_metadata[[dataset_name]], new_proc_filenames)
}

cmd <- paste('rm -r', paste0(output_path,'/','filtered_feature_bc_matrix'))
system(cmd)

procfile_md5sums <- data.frame("file name" = basename(unlist(lapply(md5sums_proc, names))),
                              "file checksum" = unlist(md5sums_proc,
                                                       use.names = FALSE), row.names = NULL, check.names = FALSE)


metadata_df <- data.frame()

for (tar_name in file_metadata) {
  sample_entry_df = data.frame(t(tar_name), check.names = FALSE)
  metadata_df <- rbind(metadata_df, sample_entry_df)
}

infolist[["Metadata"]] <- metadata_df
infolist[["Raw file md5sums"]] <- rawfile_md5sums
infolist[["Processed file md5sums"]] <- procfile_md5sums

metadata_df <- readxl::read_xlsx('/scratch/p24876_geo_upload/24876_output/infolist.xlsx')
rawfile_md5sums <- readxl::read_xlsx('/scratch/p24876_geo_upload/24876_output/rawfile_md5sums.xlsx')
procfile_md5sums <- readxl::read_xlsx('/scratch/p24876_geo_upload/24876_output/procfile_md5sums.xlsx')

writexl::write_xlsx(x = infolist, path = paste(output_path,'infolist.xlsx', sep='/'))
