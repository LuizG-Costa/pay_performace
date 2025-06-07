from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY_HEX = os.getenv("PRIVATE_KEY")  # Lemos a chave como string hexadecimal

# --- MODIFICAÇÃO AQUI ---
if PRIVATE_KEY_HEX:
    # Remove espaços em branco e '0x' se presente
    cleaned_key = PRIVATE_KEY_HEX.strip().lower()
    if cleaned_key.startswith('0x'):
        cleaned_key = cleaned_key[2:]
    
    # Verifica se tem comprimento correto (64 caracteres hex = 32 bytes)
    if len(cleaned_key) != 64:
        raise ValueError(f"Chave privada deve ter 64 caracteres hexadecimais (32 bytes). Temos {len(cleaned_key)}")
    
    PRIVATE_KEY = bytes.fromhex(cleaned_key)
else:
    raise ValueError("PRIVATE_KEY não encontrada no arquivo .env")
# --- FIM DAS MODIFICAÇÕES ---

web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# ABI e endereço do contrato (resumido aqui)
endereco_original = "0x7f5e59ce1b95accd35c1a51a2c6ebb1146fb2e7f"

if endereco_original is not None:
    endereco_original = endereco_original.strip()

endereco_original = str(endereco_original)

contract_address = Web3.to_checksum_address(endereco_original)
if not web3.is_connected():
    raise ConnectionError("❌ Não foi possível conectar à rede Sepolia.")
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

def registrar_pontuacao_blockchain(wallet_funcionario, pontos):
    try:
        conta = web3.eth.account.from_key(PRIVATE_KEY)
        nonce = web3.eth.get_transaction_count(conta.address)

        tx = contract.functions.registrarPontuacao(wallet_funcionario, int(pontos)).build_transaction({
            'from': conta.address,
            'nonce': nonce,
            'gas': 250000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })


        # Para Web3.py v6+, usamos .rawTransaction diretamente do objeto assinado
        assinado = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(assinado.raw_transaction)
        #signed_tx = conta.sign_transaction(tx)
        #tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_Transaction)


        return web3.to_hex(tx_hash)
    except Exception as e:
        return f"Erro: {e}"


def consultar_bonus_blockchain(wallet_funcionario):
    try:
        return contract.functions.calcularBonus(wallet_funcionario).call()
    except Exception as e:
        return f"Erro: {e}"

def from_wei(valor_wei):
    return web3.from_wei(valor_wei, 'ether')