class LaborType:
    UNION = "Union"
    NON_UNION = "Non-Union"

    CHOICES = (UNION, NON_UNION)

class CompanySize:
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"

    CHOICES = (SMALL, MEDIUM, LARGE)

class OperatingSystem:
    MAC = "Mac"
    PC = "Windows"

    CHOICES = (MAC, PC)