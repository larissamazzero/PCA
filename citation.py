#####################################
#####################################
## Project: PCA                    ##
##         Streamlit               ##
#####################################
## Description:                    ##
## This script was made to apply   ##
## the Inverse Laplace Transform   ##
## on CPMG, IR and SR data         ##
#####################################
## Version:  1.0                   ##
## Revision: 1.0                   ##
## Date: 07/13/2023                ##
#####################################
## Requirements:                   ##
##                                 ##
##  - matplotlib = 3.7.2		   ##
##  - numpy = 1.25.1		       ##
##  - streamlit = 1.24.1		   ##
##  - streamlit-option-menu = 0.3.6##
##  - plotly = 5.15.0       	   ##
##  - secure-smtplib = 0.1.1       ##
##  - python-dotenv = 1.0.0        ##
##                                 ##
##     //--- INTRUCTIONS ---//     ##
##                                 ##
##  pip install matplotlib==3.7.2  ##
##  pip install numpy==1.25.1      ##
##  pip install streamlit==1.24.1  ##
##  pip install streamlit-option-  ##
## menu==0.3.6                     ##
##  pip install plotly==5.15.0     ##
##  pip install secure-smtplib==0.1.1#
##  pip install python-dotenv==1.0.0#
##				                   ##
#####################################
## Script Development:             ##
##                                 ##
## - Tiago Bueno de Moraes         ##
##  [Developer]		               ##
##                                 ##
## - William Silva Mendes          ##
##  [Developer]		               ##
##                                 ##
## - Larissa Perosso Mazzero       ##
##  [Developer]		               ##
##                                 ##
##  [07/13/2023]                   ##
#####################################
## Modifications:                  ##
## 01. <NAME>                      ##
##     <COMPANY>                   ##
##     <SECTOR>                    ##
##     <DATE>                      ##
##     <MODIFICATIONS MADE>        ##
##				                   ##
##                                 ##
#####################################
#####################################

##################################
### Import Libraries
##################################
import streamlit as st

##################################
### Functions
##################################

##################################
## This function will renderizer the citation page
##
##


def citation():
    st.header("Citations")

    st.markdown("<div style='text-align:justify;'>Please cite the following reference when publishing results obtained with our WebApp. </div>", unsafe_allow_html=True)

    st.markdown("<div style='text-align:justify;'>[1] Mazzero, L.P.; Mendes, W.S.; Moraes, T.B.; A WebApp to perform the Inverse Laplace Transform of TD-NMR signals, Submetido para Computers and Electronics in Agriculture, vol. x, n. x, p. x, 2023.</div>", unsafe_allow_html=True)
      
    st.markdown("<div style='text-align:justify;'>[2] Moraes, T.B.; Transformada Inversa de Laplace para análise de sinais de Ressonância Magnética Nuclear de Baixo Campo, Química Nova, vol. 44, n. 8, p. 1020-1027, 2021. <a href='https://s3.sa-east-1.amazonaws.com/static.sites.sbq.org.br/quimicanova.sbq.org.br/pdf/v44n8a10.pdf'>(Link)</a></div>", unsafe_allow_html=True)


    
##################################

##################################
##################################
#######     CODE END       #######
##################################
##################################
