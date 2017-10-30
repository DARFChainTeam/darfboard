from openerp import models, fields, api
from openerp.tools.translate import _
import logging
# from fingerprint import Fingerprint
from dateutil import relativedelta
from datetime import datetime as dt
from dateutil import parser
import xlsxwriter
import StringIO
from io import BytesIO
import base64
import hashlib
import xmltodict
from math import modf
from lxml import etree
from xml.etree.ElementTree import fromstring
from json import dumps
import json
import requests
import base58
from subprocess import call
import subprocess
import os
import ast
from openerp.exceptions import UserError
from web3 import Web3, HTTPProvider, IPCProvider
import ipfsapi
import io
from odoo.report.preprocess import report
import xml.etree.cElementTree as ET

_logger = logging.getLogger(__name__)


class SettingOfDarfboardImport(models.Model):
    
    _name = 'setting.darfboard.import'
    
    name = fields.Char(string="Name of report for analysis")
    ethereum_pk = fields.Char(string="Ethereum smart contract address")   
    ethereum_node_address = fields.Char(string="Ethereum node address")
    ethereum_address = fields.Char(string="Smart Contract Interface")
    gas_limit = fields.Float(string='Gas limit',compute='_gas_limit')
    gas_spent = fields.Float(string='Gas will be spent',compute='_gas_spent')
    import_xml = fields.Text()
    
    
    def import_button(self):
        import_dict = {}
        address_node = self.ethereum_node_address
        web3 = Web3(HTTPProvider(address_node))
        abi_json = self.ethereum_address
        ethereum_contract_address = self.ethereum_pk
        contract =  web3.eth.contract(abi = json.loads(abi_json), address=ethereum_contract_address)
        ipfs_address = contract.call().getDocumentIPFSAddress()
        ipfs_node_api = ipfsapi.Client('localhost', 5001)
        ipfs_xml = ipfs_node_api.cat(str(ipfs_address[1:-1]))
        root = ET.fromstring(ipfs_xml)
        for item in root.iter('parameter'):
            for item_journals in item.iter('journals'):
                for item_journal in item_journals.iter('journal'):
                    for entry in item_journal.iter('entry'):
                        for item_entry in entry.findall('entry_item'):
                            print item_entry.attrib
                            import_dict.update({'parameter':item.attrib['name'],
                                                      'journal':item_journal.attrib['name'],
                                                      'entry_number':entry.attrib['number'],
                                                      'entry_date':entry.find('date').text,
                                                      'entry_item_number':item_entry.attrib['name'],
                                                      'entry_item_debit_code':float(item_entry.find('code').text),
                                                      'entry_item_debit_name':item_entry.find('name').text,
                                                      'entry_item_debit_value':float(item_entry.find('dabit').text),
                                                      'entry_item_quantity':item_entry.find('quantity').text,
                                                      'entry_item_credit_value':item_entry.find('credit').text,
                                                      })
                            
                            entry_check = self.env['data.for.analysis'].search([('entry_number','=',entry.attrib['number'])])
                            if entry_check:
                                self.env['data.for.analysis'].write(import_dict)
                            else:    
                                self.env['data.for.analysis'].create(import_dict)
                            print import_dict
        self.import_xml = ipfs_xml
                  
        
        
        
    def _gas_limit(self):
        address_node = self.ethereum_node_address
        web3 = Web3(HTTPProvider(address_node))
        abi_json = self.ethereum_address
        ethereum_contract_address = self.ethereum_pk
        print ethereum_contract_address
        contract =  web3.eth.contract(abi = json.loads(abi_json), address=ethereum_contract_address)
        try:
            result_of_gas_limit = contract.call().getGasLimit()
        except:
            result_of_gas_limit = 0
        self.gas_limit = result_of_gas_limit
    
    def _gas_spent(self):
        date_of_synchronization = dt.now()
        address_node = self.ethereum_node_address
        web3 = Web3(HTTPProvider(address_node))
        abi_json = self.ethereum_address
        ethereum_contract_address = self.ethereum_pk
        print ethereum_contract_address
        contract = web3.eth.contract(abi=json.loads(abi_json), address=ethereum_contract_address)
        hash_of_synchronaze = '"'+base58.b58encode(str(date_of_synchronization))+'"'
        print hash_of_synchronaze
        try:
            result_of_gas_estimate = contract.estimateGas().setData(str(hash_of_synchronaze))
        except:
            result_of_gas_estimate = 0
        self.gas_spent = result_of_gas_estimate
    

class DataForAnalysis(models.Model):
    
    _name = 'data.for.analysis'
    
    parameter = fields.Char(string="Parameter")
    journal = fields.Char(string="Journal")
    entry_date = fields.Date(string="Entry Date")
    entry_number = fields.Char(string="Entry code")
    entry_item_number = fields.Char(string="Entry item number")
    entry_item_debit_code = fields.Char(string="Entry debit code")
    entry_item_debit_name = fields.Char(string="Entry debit name")
    entry_item_debit_value = fields.Float(string="Debit")
    entry_item_quantity = fields.Float(string="Debit quantity")
    entry_item_credit_value = fields.Float(string="Credit")
        


    
    