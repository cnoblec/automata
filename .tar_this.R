tar <- Sys.which("tar")
if (is.na(tar) || tar == "") {
    cat("tar unavailable; cannot create tarball\n")
    quit(save = "no", status = 1, runLast = FALSE)
}


owd <- getwd()
tryCatch(finally = setwd(owd), {


    setwd(this.path::here())


    DESCRIPTION.file <- "DESCRIPTION"
    cat("* checking for file '",
        this.path::as.rel.path(this.path::here(DESCRIPTION.file), owd),
        "' ... ", sep = "")
    if (!file.exists(DESCRIPTION.file)) {
        cat("NO\n\n")
        quit(save = "no", status = 1, runLast = FALSE)
    }
    cat("OK\n")


    DESCRIPTION <- read.dcf(DESCRIPTION.file, fields = c(
        "Package",
        "Version"
    ))
    package <- DESCRIPTION[[1L, "Package"]]
    version <- DESCRIPTION[[1L, "Version"]]
    valid_package_name <- "([[:alpha:]][[:alnum:]_]*[[:alnum:]])"
    valid_package_version <- "(([[:digit:]]+[.-]){1,}[[:digit:]]+)"


    if (!is.null(problems <- c(
        if (is.na(package))
            "invalid 'Package' field\n\n",
        if (is.na(version))
            "invalid 'Version' field\n\n"
    ))) {
        cat(" ERROR\n", problems, sep = "")
        quit(save = "no", status = 1, runLast = FALSE)
    }


    cat("* checking ", DESCRIPTION.file, " meta-information ... ", sep = "")
    if (!is.null(problems <- c(
        if (!grepl(paste0("^", valid_package_name   , "$"), package))
            "Malformed package name\n\n",
        if (!grepl(paste0("^", valid_package_version, "$"), version))
            "Malformed package version.\n\n"
    ))) {
        cat("ERROR\n", problems, sep = "")
        quit(save = "no", status = 1, runLast = FALSE)
    }
    cat("OK\n")


    build.name <- paste0(
        package,
        "_",
        version,
        ".tar.gz"
    )


    # we will exclude the build itself
    exclude <- build.name


    files <- list.files(all.files = TRUE, recursive = TRUE, include.dirs = TRUE)


    # the directories to always exclude
    if (any(i <-
            (
                (basename(files) %in% c(

                    # directories from source control systems
                    "CSV", ".svn", ".arch-ids", ".bzr", ".git", ".hg",

                    # directories from eclipse
                    ".metadata",

                    "check", "chm"

                )) |

                # directories ending with Old or old
                grepl("(Old|old)$", files)
            ) & dir.exists(files))) {
        exclude <- c(exclude, files[i])
        files <- files[!i]
    }


    # the files to always exclude
    if (any(i <-
            grepl(paste0("(", c(
                "^GNUmakefile$",
                "^Read-and-delete-me$",
                "^\\.#",
                "^#", "#$",
                "~$", "\\.bak$", "\\.swp$"
            ), ")", collapse = "|"), basename(files)))) {
        exclude <- c(exclude, files[i])
        files <- files[!i]
    }


    for (exclude.pattern in paste0("^", package, "_", valid_package_version, c("\\.tar\\.gz", "\\.zip"), "$")) {
        if (any(i <- grepl(exclude.pattern, files))) {
            exclude <- c(exclude, files[i])
            files <- files[!i]
        }
    }


    ignore.file <- ".tarignore"
    if (file.exists(ignore.file)) {
        for (exclude.pattern in readLines(ignore.file, warn = FALSE, encoding = "UTF-8")) {
            if (any(i <- grepl(exclude.pattern, files, ignore.case = TRUE, perl = TRUE))) {
                exclude <- c(exclude, files[i])
                files <- files[!i]
            }
        }
    }


    exclude <- paste("--exclude", shQuote(unique(exclude)), recycle0 = TRUE)


    # transform <- paste0("--transform s,^,", package, "/")
    # args <- c("tar", exclude, transform, "-czvf", build.name, "*")


    # args <- c("tar", exclude, "-czf", build.name, "-C", "..", paste0(shQuote(basename(getwd())), "/*"))


    args <- c("tar", "-czf", build.name, exclude, "-C", "..", shQuote(basename(getwd())))
    # args <- c("tar", "-czf", FILE <- tempfile(fileext = ".tar.gz"), exclude, "-C", "..", shQuote(basename(getwd())))


    command <- paste(args, collapse = " ")


    cat("* building '", build.name, "'\n", sep = "")
    res <- system(command)
    if (res == -1L)
        stop("'", command, "' could not be run")
    else if (res)
        stop("'", command, "' execution failed with error code ", res)


})
