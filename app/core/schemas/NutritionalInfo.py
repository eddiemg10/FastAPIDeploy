from pydantic import ConfigDict, BaseModel, Field

class NutritionalInfo(BaseModel):
    value: float = Field(description="Measured value of the nutritional component", examples=[492])
    name: str = Field(description="Name of the nutritional component", examples=["Energy"])
    unit: str = Field(description="Unit of measurement used", examples=["kcal"])
    infoods_tagname: str = Field(description="International Network of Food Data Systems tagname", examples=["ENERC"])
    denominator: str = Field(description="All values have been measured with the same denomiator (/100g of Edible Portion)", examples=["/100 g EP"])
    analysis_method: str = Field(description="Analysis method used to derive the value", examples=["ISO 6496"])
    model_config = ConfigDict(from_attributes=True)
    