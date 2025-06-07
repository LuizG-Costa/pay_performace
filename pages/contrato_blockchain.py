import streamlit as st
from web3 import Web3
from dotenv import load_dotenv
import os
from utils.componentes import renderizar_sidebar



renderizar_sidebar()
# Carregar variáveis do .env
load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY_HEX = os.getenv("PRIVATE_KEY") # Lendo a chave como string hexadecimal
PRIVATE_KEY = None

if PRIVATE_KEY_HEX:
    # Remove '0x' se presente e converte de hexadecimal para bytes
    if PRIVATE_KEY_HEX.startswith('0x'):
        PRIVATE_KEY = bytes.fromhex(PRIVATE_KEY_HEX[2:])
    else:
        PRIVATE_KEY = bytes.fromhex(PRIVATE_KEY_HEX)
else:
    raise ValueError("PRIVATE_KEY não encontrada no arquivo .env")

# Conexão com a Sepolia
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not web3.is_connected():
    st.error("❌ Não foi possível conectar à rede Sepolia.")
    st.stop()

# Configuração do contrato e ABI completo
endereco_original = "0x7f5e59ce1b95accd35c1a51a2c6ebb1146fb2e7f"

# Converte para o formato de checksum
contract_address = Web3.to_checksum_address(endereco_original)
if not Web3.is_checksum_address(contract_address):
    st.error("❌ Endereço do contrato inválido.")
    st.stop()
abi = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "funcionario",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "pontos",
				"type": "uint256"
			}
		],
		"name": "registrarPontuacao",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "funcionario",
				"type": "address"
			}
		],
		"name": "resetarPontuacao",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "admin",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "funcionario",
				"type": "address"
			}
		],
		"name": "calcularBonus",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "pontuacoes",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
] 

contract = web3.eth.contract(address=contract_address, abi=abi)

st.title("📊 Gerenciar Performance via Blockchain")

# Inputs
endereco_funcionario = st.text_input("Endereço da Carteira do Funcionário (wallet Ethereum)", placeholder="0x...")
pontos = st.number_input("Pontuação a registrar", min_value=0, step=1)

# Mostrar bônus
if st.button("Consultar Bônus"):
    if endereco_funcionario:
        bonus = contract.functions.calcularBonus(endereco_funcionario).call()
        st.success(f"Bônus atual: {web3.fromWei(bonus, 'ether')} ETH")
    else:
        st.warning("Informe o endereço do funcionário.")

# Registrar pontuação
if st.button("Registrar Pontuação"):
    if not (endereco_funcionario and PRIVATE_KEY):
        st.error("Endereço e chave não fornecidos.")
    else:
        try:
            conta = web3.eth.account.from_key(PRIVATE_KEY)
            nonce = web3.eth.get_transaction_count(conta.address)
            tx = contract.functions.registrarPontuacao(endereco_funcionario, pontos).build_transaction({
                "from": conta.address,
                "nonce": nonce,
                "gas": 250000,
                "gasPrice": web3.to_wei("20", "gwei")
            })
            assinado = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = web3.eth.send_raw_transaction(assinado.rawTransaction)
            st.success(f"✅ Transação enviada: {web3.to_hex(tx_hash)}")
        except Exception as e:
            st.error(f"Erro ao registrar: {str(e)}")
