import streamlit as st 
from streamlit_option_menu import option_menu
from processing import processing 
from citation import citation
from contact import contact

with st.sidebar:
    selected = option_menu(
        menu_title="Navegation",
        options=["Home", "Processing", "Citation", "Contact"],
        icons=["house", "arrow-repeat", "quote", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    st.title('Inverse Laplace Transform (ILT)')
    r'''
    The Inverse Laplace Transform (ILT) is a mathematical transformation, which is an illposed inverse problem, 
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
if selected == "Processing":
    processing()
if selected == "Citation":
    citation()
if selected == "Contact":
    contact()
    
