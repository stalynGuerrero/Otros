# install.packages(c("readxl", "dplyr", "stringr", "bcrypt", "yaml"))

############################################
# Generar YAML de credenciales desde Excel #
############################################
# python -m streamlit run main.py

library(readxl)
library(dplyr)
library(stringr)
library(bcrypt)
library(yaml)

nueva_clave <- "Admin2026"

nuevo_hash <- hashpw(
  nueva_clave,
  gensalt(12)
)

cat(nuevo_hash)

yaml::yaml.load_file("config.yml")


#-------------------------------------------
# 1. Parámetros
#-------------------------------------------

excel_path <- "../Equipo de Campo 2026.xlsx"
sheet_name <- "usuarios"
yaml_out    <- "py/config.yaml"

bcrypt_cost <- 12  # mismo nivel que streamlit-authenticator

#-------------------------------------------
# 2. Leer Excel
#-------------------------------------------

usuarios <- read_excel(excel_path, sheet = sheet_name) %>%
  rename(
    name     = Nombre,
    email    = `Correo Electrónico`,
    username = `Usuario Reemplazo`,
    password = `Clave reemplao`,
    profile  = Perfil
  ) %>%
  mutate(
    username = str_to_lower(str_trim(username)),
    email    = str_to_lower(str_trim(email))
  )


#-------------------------------------------
# 4. Construir estructura YAML
#-------------------------------------------

credentials_list <- list(
  cookie = list(
    expiry_days = 30,
    key  = "clave_segura",
    name = "reemplazos_cookie"
  ),
  credentials = list(
    usernames = purrr::set_names(
      lapply(seq_len(nrow(usuarios)), function(i) {
        list(
          email    = usuarios$email[i],
          name     = usuarios$name[i],
          password = usuarios$password[i],
          roles    = list("user")
        )
      }),
      usuarios$username
    )
  ),
  preauthorized = list(
    emails = list()
  )
)

#-------------------------------------------
# 5. Escribir YAML
#-------------------------------------------

write_yaml(fileEncoding = "UTF-8",
  credentials_list,
  file = "py/config.yaml",
  indent = 2 
)

