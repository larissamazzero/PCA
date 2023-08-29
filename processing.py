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
##  - kaleido = 0.2.1              ##
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
## pip install kaleido==0.2.1      ##
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
import os
import io
import base64
import locale
import zipfile
import tempfile
import matplotlib
import numpy as np
import streamlit as st
from numpy import exp, log10
from datetime import datetime
from plotly.io import write_image
import plotly.graph_objects as go

##################################
### Configurations
##################################

# locale.setlocale(locale.LC_ALL, "en_US")

matplotlib.use("Agg")

##################################
### Functions
##################################

##################################
## This function will perform the Inverse Laplace Transform on data
##
##
def perform_ILT(file_path, alpha=10, dmin=0, interactions=15, points=200, Ti=0.001, Tf=10, kernel='', force=False, time_axis='seconds', normalization=False, remove_points_of_the_begin=0):

    #------------------------------------------------------------------------
    # ToolBox Laplace -  Tiago Bueno de Moraes
    #------------------------------------------------------------------------

    # Reading the data
    with open(file_path, 'r') as data:
        lines = data.readlines()
        Sig = []
        for row in lines:
            Sig.append([float(x) for x in row.split()])
        Sig = np.array(Sig)

    # Time    
    if time_axis == 'seconds':
        t = np.array(Sig[:, 0])
    elif time_axis == 'milliseconds':
        t = np.array(Sig[:, 0] / 1000)
    elif time_axis == 'microseconds':
        t = np.array(Sig[:, 0] / 1000000)

    # Signal                
    Mx = np.array(Sig[:, 1:])

    # Remove points of the begin
    if remove_points_of_the_begin != 0:
        # Verify if the number of rows to remove don't exceed the total number os rows of the signal data
        num_rows_to_remove = min(remove_points_of_the_begin, Mx.shape[0])
        Mx = Mx[num_rows_to_remove:]

    # Normalization
    if normalization == True:
        for col in range(Mx.shape[1]):
            first_element = Mx[0, col] 
            Mx[:, col] /= first_element

    # Code Start
    n = Mx.shape[0]

    T = np.logspace(log10(Ti), log10(Tf), points)

    K = []

    for i in range(0, n):
        row = []
        for j in range(0, points):
            if kernel == 'CPMG [exp(-t/T)]':
                row.append(exp(-t[i] / T[j]))

            elif kernel == 'IR [1-2*exp(-t/T)]':
                row.append(1 - 2*exp(-t[i] / T[j]))

            elif kernel == 'SR [1-exp(-t/T)]':
                row.append(1 - exp(-t[i] / T[j]))
            
        K.append(row)
    K = np.array(K)
    transposed_K = K.transpose()

    # Force to Zero
    if force == True:
        if kernel == 'CPMG [exp(-t/T)]':
            for k in range(Mx.shape[1]):
                col = len(Mx[:, k])
                media = np.mean(Mx[:, k][col-20:col], axis=0)
                for m in range(len(Mx[:, k])):
                    Mx[:, k][m] = Mx[:, k][m] - media

        elif kernel == 'IR [1-2*exp(-t/T)]':
            for k in range(Mx.shape[1]):
                col = len(Mx[:, k])
                start_value = Mx[0, k]
                end_value = Mx[col - 1, k]
                shift = (end_value + start_value) / 2
                for m in range(len(Mx[:, k])):
                    Mx[:, k][m] = Mx[:, k][m] - shift

        elif kernel == 'SR [1-exp(-t/T)]':
            for k in range(Mx.shape[1]):
                start_value = Mx[0, k]
                for m in range(len(Mx[:, k])):
                    Mx[:, k][m] = Mx[:, k][m] - start_value

    # Omega matrix
    O = K.conj().T @ K

    VV = np.zeros((len(O), len(O)))

    for k in range(1, len(O)-1):
        # VV matrix
        VVa = np.zeros((len(O), len(O)))

        VVa[k, k] = 4
        VVa[k - 1, k - 1] = 1
        VVa[k + 1, k + 1] = 1
        VVa[k + 1, k - 1] = 1
        VVa[k - 1, k + 1] = 1
        VVa[k, k + 1] = -2
        VVa[k, k - 1] = -2
        VVa[k - 1, k] = -2
        VVa[k + 1, k] = -2

        VV = VV + VVa

    VV[0, 0] = 10000000
    VV[len(O)-1, len(O)-1] = 10000000

    # Lambda matrix
    L = alpha * VV

    g = np.zeros((1, points))

    for _ in range(1, interactions + 1):
        Soma = O + L

        U, sDiag, Vh = np.linalg.svd(Soma)
        S = np.zeros(Soma.shape)
        np.fill_diagonal(S, sDiag)
        V = Vh.T.conj()

        vd = np.diag(S)
        a = len(vd)  # lenght start vd
        vd = vd.copy().reshape(points, 1)  # svd cut
        vd[vd <= dmin] = []
        np.fill_diagonal(S, vd)  # reduce S matrix

        for j in range(a, len(vd)+1, -1):
            U[:, j] = []  # delete the U matrix columns
            V[:, j] = []  # must delete the V' matrix rows

        invSoma = U @ (np.linalg.inv(S)) @ V.conj().T

        g = Mx.conj().T @ K @ invSoma

        indf = np.nonzero(g[0] < 0)
        for i in range(0, len(indf[0])):
            L[indf[0][i], indf[0][i]] = L[indf[0][i], indf[0][i]] + 10000

    # Normalization
    #g = g / np.sum(g)

    # Plotting
    # Graph 1
    fig1 = go.Figure()
    for i in range(Mx.shape[1]):
        new_Mx = Mx[:, i]
        fig1.add_trace(go.Scatter(x=t, y=new_Mx, mode='lines', name=f'Signal {i+1}'))
    fig1.update_layout(
        title=kernel,
        title_x=0.45,
        xaxis_title=f'Time ({time_axis})',
        yaxis_title='Signal Intensity (a.u.)'
    )

    # Graph 2
    def create_custom_tickvals(data, num_intervals=5):
        min_val = min(data)
        max_val = max(data)
        log_min = np.log10(min_val)
        log_max = np.log10(max_val)
        log_intervals = np.linspace(log_min, log_max, num_intervals)
        return [10**val for val in log_intervals]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=T, y=g[0], mode='lines', name='g'))
    fig2.update_layout(
    title='T2 Distribution', 
    title_x=0.45, 
    xaxis_title=f'Relaxation Time ({time_axis})', 
    yaxis_title='Signal Intensity (a.u.)', 
    xaxis_type='log')

    num_intervals = 5
    custom_tickvals = create_custom_tickvals(T, num_intervals)

    fig2.update_xaxes(
        type='log',
        tickvals=custom_tickvals,
        tickformat='.2f',  
        dtick='0.1',
    )

    # Add vertical lines for each custom tick value
    for tick_val in custom_tickvals:
        fig2.add_shape(
            type="line",
            x0=tick_val,
            x1=tick_val,
            y0=0,
            y1=1,  # Adjust the y1 value according to your plot's y-axis range
            line=dict(color="red", width=1, dash="dash")
        )

    # Graph 3
    fitting_g = np.dot(g, transposed_K)
    fitting_g = fitting_g.astype(float)
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=t, y=Mx[:, 0], mode='lines', name='Signal 1'))
    fig3.add_trace(go.Scatter(x=t, y=fitting_g[0], mode='lines', name='Fitting', line=dict(color='red')))

    fig3.update_layout(
    title='Fitting', 
    title_x=0.45, 
    xaxis_title=f'Time ({time_axis})', 
    yaxis_title='Signal Intensity (a.u.)'
    )

    # Graph 4
    residue = []  
    for col in range(Mx.shape[1]):
        column_residue = (Mx[:, col] - fitting_g)
        residue.append(column_residue)

    residue = np.array(residue[0])

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=t, y=residue[0], mode='lines', name='residues'))

    fig4.update_layout(
        title='Residues',
        title_x=0.45,
        xaxis_title=f'Time ({time_axis})',
        yaxis_title='Signal Intensity (a.u.)'
    )

    # Display graphs on Streamlit
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)

    # Generate a unique file name
    temp_file_path1 = f"temp_{np.random.randint(0, 100000)}.txt"
    temp_file_path2 = f"temp_{np.random.randint(0, 100000)}.txt"
    temp_file_path3 = f"temp_{np.random.randint(0, 100000)}.txt"

    # Saving the matrix in a temporary file 
    np.savetxt(temp_file_path1, np.vstack((T, g)).T, delimiter=" ")
    np.savetxt(temp_file_path2, fitting_g.T, delimiter=" ")
    np.savetxt(temp_file_path3, residue.T, delimiter=" ")

    # Save figures as PNG images to BytesIO objects
    fig1_bytesio = io.BytesIO()
    fig2_bytesio = io.BytesIO()
    fig3_bytesio = io.BytesIO()
    fig4_bytesio = io.BytesIO()

    # Save figures as PNG images
    fig1.write_image(fig1_bytesio, format='png')
    fig2.write_image(fig2_bytesio, format='png')
    fig3.write_image(fig3_bytesio, format='png')
    fig4.write_image(fig4_bytesio, format='png')

    # Reset BytesIO positions to the beginning
    fig1_bytesio.seek(0)
    fig2_bytesio.seek(0)
    fig3_bytesio.seek(0)
    fig4_bytesio.seek(0)

    # Return the file's path
    return temp_file_path1, temp_file_path2, temp_file_path3, fig1_bytesio, fig2_bytesio, fig3_bytesio, fig4_bytesio
##################################

##################################
## This function will create the info file
##
##
def save_info_file(file_path, alpha, ti, tf, points, kernel, force, time_axis, normalization, remove_points_of_the_begin):
    info_file_path = os.path.splitext(file_path)[0] + '_info.txt'
    link = '' #COLOCAR LINK EM PRODUÇÃO

    with open(info_file_path, 'w') as f:
        f.write('Performed by ' + str(link) + '\n')
        f.write('ILT Streamlit [...] \n\n')
        f.write('Date: ' + str(datetime.now()) + '\n\n')
        f.write('========= Pre-processing data signal =========\n\n')
        f.write('Time axis in: ' + str(time_axis) + '\n')
        f.write('Force to Zero/Center: ' + str(force) + '\n')
        f.write('Normalization: ' + str(normalization) + '\n')
        f.write('Total points of the begin removed: ' + str(remove_points_of_the_begin) + '\n\n')
        f.write('============== Parameters ====================\n\n')
        f.write('Kernel type: ' + str(kernel) + '\n')
        f.write('Alpha: ' + str(alpha) + '\n')
        f.write('Ti: ' + str(ti) + '\n')
        f.write('Tf: ' + str(tf) + '\n')
        f.write('Points: ' + str(points) + '\n\n')
        f.write('==============================================\n\n')
        f.write('Upload file: ' + file_path + '\n')

    return info_file_path
##################################

##################################
## This function will orchestrate the ILT on Streamlit
##
##
def processing():
    st.title('Inverse Laplace Transform (ILT)')

    # File upload section
    st.header('Perform the ILT on your data')
    file = st.file_uploader('Upload a TXT or DAT file', type=['txt', 'dat'])

    if 'ilt_performed' not in st.session_state:
        st.session_state['ilt_performed'] = False

    if file is not None:
        file_path = file.name
        with open(file_path, 'wb') as f:
            f.write(file.getvalue())
        
        st.header("\nSpecify input values \n\n")

        # ILT parameters
        time_axis = st.radio('**Time axis in:**', ('seconds', 'milliseconds', 'microseconds'), help='Choose the time unit for the signal.')
        with st.expander('**Pre-processing data signal**'):
            force = st.checkbox('Force to Zero/Center', value=False, help='This checkbox will force the signal to zero at the start.')
            normalization = st.checkbox('Normalization', value=False, help='This checkbox will divides the signal by the first point.')
            remove_points_of_the_begin = st.number_input('**Remove points of the begin:**', value=0, help='The number of points to remove from the beginning of the signal.')
        kernel = st.selectbox('**Kernel Type:**', ['CPMG [exp(-t/T)]', 'IR [1-2*exp(-t/T)]', 'SR [1-exp(-t/T)]'], help='The type of kernel to use.')
        alpha = st.number_input('**Alpha:**', value=1, help='The alpha value for the kernel.')
        ti = st.number_input('**Starting T value:**', value=0.001, format='%.3f', help='The starting T value for the signal.')
        tf = st.number_input('**Ending T value:**', value=10, help='The ending T value for the signal.')
        points = st.number_input('**Points:**', value=100, help='The number of points to use in the signal.')

        if st.button('Perform ILT'):
            results_file_path, fitting_file_path, residue_file_path, fig1_bytesio, fig2_bytesio, fig3_bytesio, fig4_bytesio = perform_ILT(file_path=file_path, alpha=alpha, Ti=ti, Tf=tf, points=points, kernel=kernel, force=force, time_axis=time_axis, normalization=normalization, remove_points_of_the_begin=remove_points_of_the_begin)
            info_file_path = save_info_file(file_path, alpha, ti, tf, points, kernel, force, time_axis, normalization, remove_points_of_the_begin)
            st.session_state['ilt_performed'] = True

            if st.session_state['ilt_performed']:
                st.success('Inverse Laplace Transform function performed successfully!')
                
                # Zip file with results
                zip_file = io.BytesIO()
                with zipfile.ZipFile(zip_file, 'w') as zf:
                    zf.writestr('ILT_results.txt', open(results_file_path, 'r').read())
                    zf.writestr('Fitting.txt', open(fitting_file_path, 'r').read())
                    zf.writestr('Residues.txt', open(residue_file_path, 'r').read())
                    zf.writestr('ILT_info.txt', open(info_file_path, 'r').read())
                    # Add the figures to the zip file
                    zf.writestr('Signal.png', fig1_bytesio.read())
                    zf.writestr('T2_Distribution.png', fig2_bytesio.read())
                    zf.writestr('Fitting.png', fig3_bytesio.read())
                    zf.writestr('Residues.png', fig4_bytesio.read())
                zip_file.seek(0)

                # Download buttom
                st.download_button(label='Download ILT Files', data=zip_file, file_name='ILT_files.zip', mime='application/zip')
##################################

##################################
##################################
#######     CODE END       #######
##################################
##################################
