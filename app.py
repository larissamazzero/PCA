#####################################
#####################################
## Project: ILT                    ##
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
from streamlit_option_menu import option_menu
from processing import processing 
from citation import citation
from contact import contact

st.set_page_config(layout="centered", 
                   page_title="Inverse Laplace Transform", 
                   page_icon="chart_with_upwards_trend"
                   )
##################################
### Configurations
##################################

with st.sidebar:
    selected = option_menu(
        menu_title="Navegation",
        options=["Home", "Processing", "Citation", "Contact"],
        icons=["house", "arrow-repeat", "quote", "envelope"],
        menu_icon="cast",
        default_index=0,
    )
    st.info("This web platform is free and open source and you are very welcome to contribute. Please contact us!")

##################################
## This function will orchestrate the Streamlit App
##
##
if selected == "Home":
    st.title('Inverse Laplace Transform (ILT)')
    r'''
    The **Inverse Laplace Transform (ILT)** is a mathematical transformation, which is an illposed inverse problem, 
    that can admit multiple solutions, where the general objective is to start from a signal in the time domain $$A(t)$$
    we want to obtain the distribution of relaxation times $$g(T)$$.
        '''

    r'''
    In the case of a CPMG experiment, we have: $$A(t) = \sum_{j=1}^{N} g(T_{2}). K(t_{n},T_{2j}) dt + ϵ_{n}$$
    where $K(t_{n},T_{2j})$ is the kernel matrix, which depends on the type of signal being analyzed (CPMG -> exponential decays).
    '''

    r'''
    In the example in Figure 1 we have the input signal $$A(t)$$ which is a mixture of exponentials decaying in time, and the transformation by ILT will 
    reveal in the domain of relaxation rates, what the relaxation times are $$T_{2}$$ and their amplitudes.
    '''

    r'''
    More information can be found in this [video about ILT](https://www.youtube.com/watch?v=aobB016VhXs&list=PL2LQTWHzmXcC8SIW6cjPpEapv1kPeQWOi&index=4), or in our article:
    '''

    r'''
    *Moraes, T.B.; *Transformada Inversa de Laplace para análise de sinais de Ressonância Magnética Nuclear de Baixo Campo, *Química Nova*, vol. 44, n. 8, p. 1020-1027, 2021. ([Link](http://dx.doi.org/10.21577/0100-4042.20170751))
    '''
    st.markdown("[![ILT.png](https://i.postimg.cc/W1HxWjw9/ILT.png)](https://postimg.cc/PC16JgcZ)")
    st.write("_**Figure 1.** ILT process_")

    st.subheader("Suporters")
    st.write("Developed by T. B. Moraes, L. P. Mazzero, W. S. Mendes")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("[![CNPQ.jpg](https://i.postimg.cc/6Q2rHQNN/CNPQ.jpg)](http://portal.cnpq.br/)")
        st.markdown("\n")
        st.markdown("\n")
        st.markdown("[![ESALQ.png](https://i.postimg.cc/4dKbxkDS/ESALQ.png)](https://www.esalq.usp.br/)")
    with col2:
        st.markdown("[![IFSP.png](https://i.postimg.cc/3RWxjyMg/ifsp.jpg)](https://prc.ifsp.edu.br/)")
    with col3:
        st.markdown("[![USP.jpg](https://i.postimg.cc/jqBddKRy/USP.jpg)](https://www5.usp.br/)")
   
if selected == "Processing":
    processing()
if selected == "Citation":
    citation()
if selected == "Contact":
    contact()



##################################

##################################
##################################
#######     CODE END       #######
##################################
##################################    
