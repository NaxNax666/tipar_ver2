from web3 import Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy

abi = """[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "summ_return",
				"type": "uint256"
			}
		],
		"name": "breakRental",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "endRental",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "isActive",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "car",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "_seller",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_totalcost",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_zalog",
				"type": "uint256"
			}
		],
		"name": "startRental",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	}
]"""
bytecode = "608060405234801561001057600080fd5b50610d66806100206000396000f3fe60806040526004361061003f5760003560e01c806322f3e2d4146100445780632f03c0371461006f5780636ebd1b4314610086578063fc56bcd0146100af575b600080fd5b34801561005057600080fd5b506100596100cb565b60405161006691906107b3565b60405180910390f35b34801561007b57600080fd5b506100846100de565b005b34801561009257600080fd5b506100ad60048036038101906100a89190610818565b61032a565b005b6100c960048036038101906100c491906109e9565b61069b565b005b600560009054906101000a900460ff1681565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161461016c576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161016390610aef565b60405180910390fd5b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166003546040516101b590610b40565b60006040518083038185875af1925050503d80600081146101f2576040519150601f19603f3d011682016040523d82523d6000602084013e6101f7565b606091505b505090508061023b576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161023290610ba1565b60405180910390fd5b6000600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1660045460405161028590610b40565b60006040518083038185875af1925050503d80600081146102c2576040519150601f19603f3d011682016040523d82523d6000602084013e6102c7565b606091505b505090508061030b576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161030290610ba1565b60405180910390fd5b6000600560006101000a81548160ff0219169083151502179055505050565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146103b8576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016103af90610aef565b60405180910390fd5b6003548111156103fd576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016103f490610c0d565b60405180910390fd5b60008160035461040d9190610c5c565b90506000600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168360405161045790610b40565b60006040518083038185875af1925050503d8060008114610494576040519150601f19603f3d011682016040523d82523d6000602084013e610499565b606091505b50509050806104dd576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016104d490610ba1565b60405180910390fd5b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1660045460405161052690610b40565b60006040518083038185875af1925050503d8060008114610563576040519150601f19603f3d011682016040523d82523d6000602084013e610568565b606091505b50509050806105ac576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016105a390610ba1565b60405180910390fd5b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16846040516105f390610b40565b60006040518083038185875af1925050503d8060008114610630576040519150601f19603f3d011682016040523d82523d6000602084013e610635565b606091505b5050905080610679576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161067090610ba1565b60405180910390fd5b6000600560006101000a81548160ff0219169083151502179055505050505050565b3481836106a89190610c90565b146106e8576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016106df90610d10565b60405180910390fd5b826000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555033600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555081600381905550806004819055506001600560006101000a81548160ff02191690831515021790555050505050565b60008115159050919050565b6107ad81610798565b82525050565b60006020820190506107c860008301846107a4565b92915050565b6000604051905090565b600080fd5b600080fd5b6000819050919050565b6107f5816107e2565b811461080057600080fd5b50565b600081359050610812816107ec565b92915050565b60006020828403121561082e5761082d6107d8565b5b600061083c84828501610803565b91505092915050565b600080fd5b600080fd5b6000601f19601f8301169050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6108988261084f565b810181811067ffffffffffffffff821117156108b7576108b6610860565b5b80604052505050565b60006108ca6107ce565b90506108d6828261088f565b919050565b600067ffffffffffffffff8211156108f6576108f5610860565b5b6108ff8261084f565b9050602081019050919050565b82818337600083830152505050565b600061092e610929846108db565b6108c0565b90508281526020810184848401111561094a5761094961084a565b5b61095584828561090c565b509392505050565b600082601f83011261097257610971610845565b5b813561098284826020860161091b565b91505092915050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b60006109b68261098b565b9050919050565b6109c6816109ab565b81146109d157600080fd5b50565b6000813590506109e3816109bd565b92915050565b60008060008060808587031215610a0357610a026107d8565b5b600085013567ffffffffffffffff811115610a2157610a206107dd565b5b610a2d8782880161095d565b9450506020610a3e878288016109d4565b9350506040610a4f87828801610803565b9250506060610a6087828801610803565b91505092959194509250565b600082825260208201905092915050565b7f4f6e6c792073656c6c65722063616e20706572666f726d20746869732061637460008201527f696f6e0000000000000000000000000000000000000000000000000000000000602082015250565b6000610ad9602383610a6c565b9150610ae482610a7d565b604082019050919050565b60006020820190508181036000830152610b0881610acc565b9050919050565b600081905092915050565b50565b6000610b2a600083610b0f565b9150610b3582610b1a565b600082019050919050565b6000610b4b82610b1d565b9150819050919050565b7f5472616e73666572206661696c65642e00000000000000000000000000000000600082015250565b6000610b8b601083610a6c565b9150610b9682610b55565b602082019050919050565b60006020820190508181036000830152610bba81610b7e565b9050919050565b7f496e76616c69642073756d000000000000000000000000000000000000000000600082015250565b6000610bf7600b83610a6c565b9150610c0282610bc1565b602082019050919050565b60006020820190508181036000830152610c2681610bea565b9050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b6000610c67826107e2565b9150610c72836107e2565b9250828203905081811115610c8a57610c89610c2d565b5b92915050565b6000610c9b826107e2565b9150610ca6836107e2565b9250828201905080821115610cbe57610cbd610c2d565b5b92915050565b7f4c6f772077656900000000000000000000000000000000000000000000000000600082015250565b6000610cfa600783610a6c565b9150610d0582610cc4565b602082019050919050565b60006020820190508181036000830152610d2981610ced565b905091905056fea26469706673582212208a282dd92b2f82514c57422ff8c4b636158448493379d3cf58c41d980f670db664736f6c63430008120033"


class Contracts:
    def __init__(self):
        http = 'http://93.95.97.136:8545/'
        self.w3 = Web3(Web3.HTTPProvider(http))
        self.seller_account_list = {}
        self.user_account_list = {}
        self.w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
        self.rent_contract_list = {}
        self.chainID = 51515
        self.adminWallet = {
            'private_key': "YOUR PRIVATE KEY HERE",
            'address': 'YOUR CONTRACT ADDRESS HERE',
        }

    def sign_up(self):
        acc = self.w3.eth.account.create()
        return acc

    def start_rent(self, seller, user, rent, days, car):
        nonce = self.w3.eth.get_transaction_count(self.adminWallet['address'])
        contract_inst = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        transaction = contract_inst.constructor().build_transaction({
            "gasPrice": self.w3.eth.gas_price,
            "chainId": self.chainID,
            "from": self.adminWallet["address"],
            "nonce": nonce

        })
        sign_transaction = self.w3.eth.account.sign_transaction(transaction,
                                                                private_key=self.adminWallet["private_key"])
        transaction_hash = self.w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
        trasaction_recepit = self.w3.eth.wait_for_transaction_receipt(transaction_hash)
        contractAddress = trasaction_recepit["contractAddress"]

        npay_contract_inst = self.w3.eth.contract(address=contractAddress, abi=abi)
        token_supply = npay_contract_inst.functions.startRental(car.name, seller["address"], rent * days,
                                                                rent * 10).build_transaction(
            {
                'chainId': self.chainID,
                'nonce': self.w3.eth.get_transaction_count(user['address']),
                'gasPrice': self.w3.eth.generate_gas_price(),
                'gas': 70000,
                'value': rent * days + rent * 10,
            })
        tx_create = self.w3.eth.account.sign_transaction(token_supply, user['private_key'])
        tx_hash = self.w3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return [tx_hash, contractAddress]

    def endRental(self, seller, contractAddress):
        npay_contract_inst = self.w3.eth.contract(address=contractAddress, abi=abi)
        token_supply = npay_contract_inst.functions.endRental().build_transaction(
            {
                'chainId': self.chainID,
                'nonce': self.w3.eth.get_transaction_count(seller['address']),
                'gasPrice': self.w3.eth.generate_gas_price(),
                'gas': 70000,
            })
        tx_create = self.w3.eth.account.sign_transaction(token_supply, seller['private_key'])
        tx_hash = self.w3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def breakRental(self, seller, contractAddress, summ_to_return):
        npay_contract_inst = self.w3.eth.contract(address=contractAddress, abi=abi)
        token_supply = npay_contract_inst.functions.breakRental(summ_to_return).build_transaction(
            {
                'chainId': self.chainID,
                'nonce': self.w3.eth.get_transaction_count(seller['address']),
                'gasPrice': self.w3.eth.generate_gas_price(),
                'gas': 70000,
            })
        tx_create = self.w3.eth.account.sign_transaction(token_supply, seller['private_key'])
        tx_hash = self.w3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def getbalance(self, user):
        return self.w3.from_wei(self.w3.eth.get_balance(user), 'ether')

    def getreipt(self, tx_hash):
        return self.w3.eth.get_transaction_receipt(tx_hash)

    def transfer(self, tgt, amount):
        print('infunc')
        tx_create = self.w3.eth.account.sign_transaction(
            {
                'chainId': self.chainID,
                'nonce': self.w3.eth.get_transaction_count(self.adminWallet['address']),
                'gasPrice': self.w3.eth.generate_gas_price(),
                'gas': 70000,
                'to': tgt,
                'value': self.w3.to_wei(str(amount), 'ether'),
            },
            self.adminWallet['private_key'],
        )
        print('tx_done')
        tx_hash = self.w3.eth.send_raw_transaction(tx_create.rawTransaction)
        print('th_send')
        return tx_hash

