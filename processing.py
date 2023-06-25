import os
import io
import zipfile
import numpy as np
import matplotlib
import streamlit as st
from numpy import exp, log10
from datetime import datetime
from matplotlib import pyplot as plt

st.set_page_config(layout="centered")
matplotlib.use("Agg")

def perform_ILT(file_path, alpha=10, dmin=0, interactions=15, points=200, Ti=0.001, Tf=10):

    #------------------------------------------------------------------------
    # ToolBox Laplace -  Tiago Bueno de Moraes
    #------------------------------------------------------------------------

    # Leitura dados
    with open(file_path, 'r') as data:
        Sig = []
        for row in data:
            Sig.append([float(x) for x in row.split()])
        Sig = np.array(Sig)

    t = np.array(Sig[:, 0] / 1000)
    Mx = np.array(Sig[:, 1])
    My = np.zeros(np.size(Mx))

    # Início Código
    n = len(Mx)

    T = np.logspace(log10(Ti), log10(Tf), points)

    K = []
    for i in range(0, n):
        row = []
        for j in range(0, points):
            row.append(exp(-t[i] / T[j]))
        K.append(row)
    K = np.array(K)

    # matriz Omega
    O = K.conj().T @ K

    VV = np.zeros((len(O), len(O)))

    for k in range(1, len(O)-1):
        # matriz VV
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

    # matriz Lambda
    L = alpha * VV

    g = np.zeros((1, points))

    for inte in range(1, interactions + 1):
        Soma = O + L

        U, sDiag, Vh = np.linalg.svd(Soma)
        S = np.zeros(Soma.shape)
        np.fill_diagonal(S, sDiag)
        V = Vh.T.conj()

        vd = np.diag(S)
        a = len(vd)  # tamanho vd inicio
        vd = vd.copy().reshape(200, 1)  # corte svd
        vd[vd <= dmin] = []
        np.fill_diagonal(S, vd)  # matriz S reduzida

        for j in range(a, len(vd)+1, -1):
            U[:, j] = []  # eliminar colunas da matriz U
            V[:, j] = []  # temos que eliminar as linhas da matriz V'

        invSoma = U @ (np.linalg.inv(S)) @ V.conj().T

        g = Mx.conj().T @ K @ invSoma

        indf = np.nonzero(g < 0)
        for i in range(0, len(indf)):
            L[indf[i], indf[i]] = L[indf[i], indf[i]] + 10000

    # Normalização
    g = g / np.sum(g)

    # Plotting
    fig1 = plt.figure(figsize=(10, 10))

    ax1 = fig1.add_subplot(2, 2, 1)
    ax1.plot(t, Mx, t, My)
    ax1.set_title('CPMG')

    ax2 = fig1.add_subplot(2, 2, 2)
    ax2.stem(range(1, len(S) + 1), vd)
    ax2.set_title('Valores Singulares')
    ax2.set_yscale('log')

    ax3 = fig1.add_subplot(2, 1, 2)
    ax3.plot(T, g)
    ax3.set_title('Distribuição T2')
    ax3.set_xlim(Ti, Tf)
    ax3.set_xscale('log')

    st.pyplot(fig1)

    # Gerar um nome de arquivo único
    temp_file_path = f"temp_{np.random.randint(0, 100000)}.txt"

    # Salvar a matriz em um arquivo temporário
    np.savetxt(temp_file_path, np.vstack((T, g)).T, delimiter=" ")

    # Retorna o caminho do arquivo temporário
    return temp_file_path

def save_info_file(file_path, alpha, dmin, interactions, points):
    info_file_path = os.path.splitext(file_path)[0] + '_info.txt'

    with open(info_file_path, 'w') as f:
        f.write('Date: ' + str(datetime.now()) + '\n')
        f.write('ILT Streamlit [...] \n\n')
        f.write('Parameters:\n')
        f.write('Alpha: ' + str(alpha) + '\n')
        f.write('Dmin: ' + str(dmin) + '\n')
        f.write('Interactions: ' + str(interactions) + '\n')
        f.write('Points: ' + str(points) + '\n\n')
        f.write('Upload file: ' + file_path + '\n')

    return info_file_path
    
def processing():
    st.title('Inverse Laplace Transform (ILT)')

    # File upload section
    st.header('Upload File')
    file = st.file_uploader('Upload a TXT or CSV file', type=['txt', 'csv'])

    if 'ilt_performed' not in st.session_state:
        st.session_state['ilt_performed'] = False

    if file is not None:
        file_path = file.name
        with open(file_path, 'wb') as f:
            f.write(file.getvalue())

        # ILT parameters
        alpha = st.number_input('Alpha', min_value=0, max_value=100, value=10)
        dmin = st.number_input('Dmin', min_value=0, max_value=10, value=0)
        interactions = st.number_input('Interactions', min_value=1, max_value=30, value=15)
        points = st.number_input('Points', min_value=50, max_value=500, value=200)

        if st.button('Perform ILT'):
            modified_file_path = perform_ILT(file_path, alpha, dmin, interactions, points)
            info_file_path = save_info_file(file_path, alpha, dmin, interactions, points)
            st.success('ILT performed successfully!')
            st.session_state['ilt_performed'] = True

            if st.session_state['ilt_performed']:
                # Zip file with results
                zip_file = io.BytesIO()
                with zipfile.ZipFile(zip_file, 'w') as zf:
                    zf.writestr('ILT_results.txt', open(modified_file_path, 'r').read())
                    zf.writestr('ILT_info.txt', open(info_file_path, 'r').read())
                zip_file.seek(0)

                # Download buttom
                st.download_button(label='Download ILT Files', data=zip_file, file_name='ILT_files.zip', mime='application/zip')


# if __name__ == '__main__':
#     main()
