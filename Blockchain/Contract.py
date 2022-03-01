from web3 import Web3
from solcx import compile_files


class Contract():
    def __init__(self, contract_name, contract_file, *,
                 base_path='.',
                 import_remappings=None, **kwargs
                 ):
        contract_file = contract_file.lstrip("./")
        compiled_sol = compile_files(
            contract_file,
            output_values=["abi", "bin"],
            base_path='.',
            import_remappings=import_remappings,
            **kwargs)

        # print(compiled_sol)
        # print(compiled_sol["contracts/Aaa.sol:Artopus"])
        contract_interface = compiled_sol[f"{contract_file}:{contract_name}"]
        self.bytecode = contract_interface['bin']
        # get abi
        self.abi = contract_interface['abi']


if __name__ == "__main__":
    import sys
    c = Contract("Artopus", sys.argv[1], import_remappings={
        "@openzeppelin": "/node_modules/@openzeppelin"})
    print(c.bytecode)
