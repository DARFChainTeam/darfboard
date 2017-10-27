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

_logger = logging.getLogger(__name__)


class SettingOfJournals(models.Model):
    
    _name = 'setting.journals'
    
    name = fields.Char(string="Name of report for analysis")
    list_of_parameters = fields.One2many('list.of.parameters','parameter_id') 
    ethereum_pk = fields.Char(string="Ethereum smart contract address")   
    ethereum_node_address = fields.Char(string="Ethereum node address")
    ethereum_address = fields.Char(string="Smart Contract Interface")
    gas_limit = fields.Float()
    gas_spent = fields.Float()
    send_period = fields.Selection([
            ('day', 'Every day'),
            ('week', 'Weekly'),
            ('month','Monthly'),
            ('Period','Time period of synchronization')],string="Period of synchronization")
    week_day = fields.Selection([
            ('0', 'Mn'),
            ('1', 'Tu'),
            ('2', 'We'),
            ('3', 'Th'),
            ('4', 'Fr'),
            ('5', 'Sd'),
            ('6', 'Sun')
        ],
        string="Day of week")
    send_time = fields.Float(string="Time")
    time_period = fields.Float(string="Time period")
    send_date = fields.Integer(string='Day of month')
    last_send_date = fields.Date(string="Date of last synchronization")
    last_send_time = fields.Float(string="Time of last synchronization")
    xml_for_synchronization = fields.Text(string="XML for synchronization")
    
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
        if self.import_export == 'export':
            try:
                result_of_gas_estimate = contract.estimateGas().setData(str(hash_of_synchronaze))
            except:
                result_of_gas_estimate = 0
        if self.import_export == 'import':
            try:
                result_of_gas_estimate = contract.estimateGas().HashOfDB()
            except:
                result_of_gas_estimate = 0
        self.gas_spent = result_of_gas_estimate
    
    def sand_report(self):
        print "test sand report"
        date_of_synchronization = dt.now()
        general_info_text = str(date_of_synchronization)
        root = etree.Element("data")
        general_info = etree.SubElement(root,'general_info')
        general_info.text=general_info_text
        #------------------------------------------ create subelement for report
        report = etree.SubElement(root, 'report')
        report.set("name",self.name)
        
        for item_list in self.list_of_parameters:
            parameter = etree.SubElement(report,'parameter')
            parameter.set("name",item_list.name)
            
        self.xml_for_synchronization = etree.tostring(root, pretty_print=True)
        
        
        
class ListOfParameter(models.Model):
    
    _name='list.of.parameters'
    
    name = fields.Char()
    parameter_id = fields.Many2one('setting.journal',default=lambda self: self._context.get('parameter_id', self.env['setting.journals']))
    journal_list = fields.Many2many('account.journal',string="Select Journal for analysis")

