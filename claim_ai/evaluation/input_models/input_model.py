import pandas

from .mixins import DataFrameRepresentationMixin


class BaseModel:

    def __init__(self, **fields):
        for field, value in fields.items():
            if hasattr(self, field):
                setattr(self, field, value)
            else:
                raise ValueError(F"Field {field} not available for class {self.__class__}")

    def to_representation(self) -> pandas.DataFrame:
        raise NotImplementedError("to_ai_input_representation not implemented")


class BaseDataFrameModel(DataFrameRepresentationMixin, BaseModel):
    alias = {}

    def alias_or_default(self, name):
        return self.alias.get(name, name)

    def to_dict(self, use_alias=True):
        dict_ = {}
        for k, v in self.__dict__.items():
            k = self.alias.get(k, k) if use_alias else k
            dict_[k] = v
        return dict_


class ProvidedItem(BaseDataFrameModel):
    identifier = None
    unit_price = None
    frequency = None
    use_context = None
    item_level = None
    quantity = None
    price_asked = None

    alias = {
        'identifier': 'ItemUUID',
        'unit_price': 'ItemPrice',
        'frequency': 'ItemFrequency',
        'use_context': 'ItemPatCat',
        'item_level': 'ItemLevel',
        'type': 'ItemServiceType',
        'quantity': 'QtyProvided',
        'price_asked': 'PriceAsked',
    }


class Medication(ProvidedItem):
    def __init__(self, **fields):
        super().__init__(**fields)
        self.type = 'Medication'  # fixed
        self.item_level = 'M'


class ActivityDefinition(ProvidedItem):
    def __init__(self, **fields):
        super().__init__(**fields)
        self.type = 'ActivityDefinition'  # fixed
        self.item_level = 'S'  # fixed


class Claim(BaseDataFrameModel):
    identifier = None
    billable_period_from = None
    billable_period_to = None
    created = None
    type = None
    diagnosis_0 = None
    diagnosis_1 = None
    enterer = None

    alias = {
        'identifier': 'ClaimUUID',
        'billable_period_from': 'DateFrom',
        'billable_period_to': 'DateTo',
        'created': 'DateClaimed',
        'type': 'VisitType',
        'diagnosis_0': 'ICDID',
        'diagnosis_1': 'ICDID1',
        'enterer': 'ClaimAdminUUID'
    }


class Patient(BaseDataFrameModel):
    identifier = None
    birth_date = None
    gender = None
    is_head = None
    location_code = None

    alias = {
        'identifier': 'InsureeUUID',
        'birth_date': 'DOB',
        'gender': 'Gender',
        'is_head': 'IsHead',  # This value is not present in the AiModel
        'location_code': 'LocationUUID',
    }


class Group(BaseDataFrameModel):
    group = None
    poverty_status = None

    alias = {
        'group': 'FamilyUUID',
        'poverty_status': 'PovertyStatus',  # This value is not present in the AiModel
    }


class HealthcareService(BaseDataFrameModel):
    identifier = None
    location = None
    category = None
    type = None

    alias = {
        'identifier': 'HFUUID',
        'location': 'HFLocationUUID',
        'category': 'HFLevel',
        'type': 'HFCareType'
    }


class AiInputModel(BaseDataFrameModel):
    medication = None
    activity_definition = None
    claim = None
    patient = None
    group = None
    healthcare_service = None

    def to_representation(self, flat=False):
        df = pandas.DataFrame()
        if flat:
            out = {}
            for next_entry in self.__dict__.values():
                if next_entry:
                    for k, v in next_entry.__dict__.items():
                        k = next_entry.alias_or_default(k)
                        out[k] = v
            return out

        for variable, value in self.__dict__.items():
            variable_frame = value.to_representation() if value else pandas.DataFrame()  # empty dataframe if empty
            # Remove index
            variable_frame.reset_index(inplace=True, drop=True)
            df = pandas.concat([df, variable_frame], axis=1)
        return df
