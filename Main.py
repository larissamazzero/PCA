import streamlit as st
from matplotlib import pyplot as plt
import numpy as np
from numpy import exp, log10
import matplotlib

matplotlib.use("Agg")

def perform_ILT(file_path, alpha=10, dmin=0, interacoes=15, pontos=200, Ti=0.001, Tf=10):

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

    T = np.logspace(log10(Ti), log10(Tf), pontos)

    K = []
    for i in range(0, n):
        row = []
        for j in range(0, pontos):
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

    g = np.zeros((1, pontos))

    for inte in range(1, interacoes + 1):
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
    np.savetxt(temp_file_path, np.vstack((T, g)), delimiter=" ")

    # Retorna o caminho do arquivo temporário
    return temp_file_path


def main():
    st.title('Inverse Laplace Transform (ILT)')

    # Info section
    st.markdown('<div style="text-align: justify;">The <strong>Inverse Laplace Transform (ILT)</strong> is a mathematical transformation, which is an illposed inverse problem, that can admit multiple solutions, where the general objective is to start from a signal in the time domain </div>', unsafe_allow_html=True)
    st.latex(r'''A(t)''')
    # File upload section
    st.header('Upload File')
    file = st.file_uploader('Upload a TXT or CSV file', type=['txt', 'csv'])

    if file is not None:
        file_path = file.name
        with open(file_path, 'wb') as f:
            f.write(file.getvalue())

        # ILT parameters
        alpha = st.slider('Alpha', min_value=0, max_value=100, value=10)
        dmin = st.slider('Dmin', min_value=0, max_value=10, value=0)
        interacoes = st.slider('Interacoes', min_value=1, max_value=30, value=15)
        pontos = st.slider('Pontos', min_value=50, max_value=500, value=200)

        if st.button('Perform ILT'):
            modified_file_path = perform_ILT(file_path, alpha, dmin, interacoes, pontos)
            st.success('ILT performed successfully!')
            st.download_button(label='Download ILT performed', data=open(modified_file_path, 'rb').read(), file_name="ILT_file.txt", mime="text/plain")


if __name__ == '__main__':
    main()