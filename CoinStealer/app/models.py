import uuid
import datetime
from functools import reduce
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.orm import backref

class User(Base):
    __tablename__ = 'users'
    username = Column(String(50), primary_key=True, unique=True)
    password = Column(String(50))
    admin = Column(Boolean, default=False)
    wallet = relationship('MultiSigWallet', uselist=False)
    def __init__(self, username, password):
        self.username = username
        self.password = password
        signaturesInit = [WalletSignature(uuid.uuid4().hex), WalletSignature(uuid.uuid4().hex), WalletSignature(uuid.uuid4().hex)]
        self.wallet = MultiSigWallet(signatures = signaturesInit)
    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.username)
    
class MultiSigWallet(Base):
    __tablename__ = 'multisigwallets'
    wallet_uuid =   Column(String(32), primary_key=True, unique=True, default=uuid.uuid4().hex)
    user_username = Column(String(50), ForeignKey('users.username'), unique=True)
    signatures = relationship("WalletSignature")
    total_signatures = Column(Integer)
    required = Column(Integer)

    def __init__(self, wallet_uuid = uuid.uuid4().hex, signatures = [], total_signatures = 3, required = 2):
        self.wallet_uuid = wallet_uuid
        self.total_signatures = total_signatures
        self.required = required
        for signature in signatures:
            self.signatures.append(signature)

    def __repr__(self):
        return '<MultiSigWallet {} Total Signatures: {}>'.format(self.wallet_uuid, self.total_signatures)

    def validateSignatures(self, signsToEval):
        correctSigns = 0
        for sign in signsToEval:
            for signature in self.signatures:
                if sign.signature == signature.signature:
                    correctSigns += 1
        
        if correctSigns >= self.required:
            return True
        else:
            return False
    
    @property
    def value(self):
        transactions = self.transactions
        if len(transactions) <= 0:
            return 0
        transactionsValues = list(map(lambda transaction: transaction.value, transactions))
        return reduce(lambda total, val: total+val, transactionsValues)

    @property
    def transactions(self):
        allTransactions = Transaction.query.all()
        return list(filter(lambda transaction: self.validateSignatures(transaction.signatures), allTransactions))

class Signature(Base):
    __tablename__ = 'signatures'
    sig_uuid = Column(String(32), primary_key=True, default=uuid.uuid4().hex)
    signature = Column(String(128))
    
    def __init__(self):
        self.sig_uuid = uuid.uuid4().hex 


class WalletSignature(Signature):
    # __tablename__ = 'walletsigs'
    parent_wallet_uuid = Column(String(32), ForeignKey('multisigwallets.wallet_uuid'))

    def __init__(self, signature = uuid.uuid4().hex): 
        self.sig_uuid = uuid.uuid4().hex
        self.signature = signature

    def __repr__(self):
        return '<WalletSignature {}>'.format(self.signature)


class TransactionSignature(Signature):       
    # __tablename__ = 'transactionsigs'
    parent_transaction_uuid = Column(String(32), ForeignKey('transactions.transaction_uuid'))

    def __init__(self, signature = uuid.uuid4().hex): 
        self.sig_uuid = uuid.uuid4().hex
        self.signature = signature

    def __repr__(self):
        return '<TransactionSignature {}>'.format(self.signature)


class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_uuid = Column(String(32), primary_key=True, unique=True)
    signatures = relationship('TransactionSignature')
    value = Column(Integer)

    def __init__(self, signatures = None, value = 0):
        self.transaction_uuid = uuid.uuid4().hex
        self.value = value
        for signature in signatures:
            self.signatures.append(TransactionSignature(signature.signature))

    def __repr__(self):
        return '<Transaction {} Value: {}>'.format(self.transaction_uuid, self.value)
