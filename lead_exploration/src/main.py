from dataclasses import dataclass
from bakery import assert_equal  # type: ignore
from lead import de_school_lead_samples

LINE1 = """0002ppb| Appoquinimink|               Alfred G Waters Middle School|Kitchen Faucet"""
LINE2 = """0002ppb| Appoquinimink|               Alfred G Waters Middle School|Water Bottle Filler Cafeteria"""
LINE3 = """0160ppb|Sussex Vo-Tech|                                 Sussex Tech|Water Spigot In the Field"""

LINES = [LINE1, LINE2, LINE3]


@dataclass(frozen=True)
class Sample:
    level: int  # ppb
    district: str
    school: str
    location: str


SAMPLE1 = Sample(
    level=2,
    district="Appoquinimink",
    school="Alfred G Waters Middle School",
    location="Kitchen Faucet",
)

SAMPLE2 = Sample(
    level=2,
    district="Appoquinimink",
    school="Alfred G Waters Middle School",
    location="Water Bottle Filler Cafeteria",
)

SAMPLE3 = Sample(
    level=160,
    district="Sussex Vo-Tech",
    school="Sussex Tech",
    location="Water Spigot In the Field",
)


SAMPLES = [SAMPLE1, SAMPLE2, SAMPLE3]


def convert_line(line: str) -> Sample:
    return Sample(
        level=int(line[0:4]),
        district=line[8:22].strip(),
        school=line[23:67].strip(),
        location=line[68:].strip(),
    )


assert_equal(convert_line(LINE1), SAMPLE1)
assert_equal(convert_line(LINE2), SAMPLE2)
assert_equal(convert_line(LINE3), SAMPLE3)


def convert_lines(lines: list[str]) -> list[Sample]:
    return [convert_line(line) for line in lines]


assert_equal(convert_lines(LINES), SAMPLES)


def total_lead(
    samples: list[Sample],
) -> int:
    levels = [sample.level for sample in samples]
    return sum(levels)


assert_equal(total_lead([]), 0)
assert_equal(total_lead([SAMPLE1]), 2)
assert_equal(total_lead(SAMPLES), 164)


def average_lead(
    samples: list[Sample],
) -> float:
    if len(samples) == 0:
        return 0.0

    return total_lead(samples) / len(samples)


assert_equal(average_lead([]), 0.0)
assert_equal(average_lead([SAMPLE1]), 2.0)
assert_equal(average_lead(SAMPLES), 164 / 3)


def average_lead_per_district(
    samples: list[Sample],
    district: str,
) -> float:
    samples_from_district = [
        sample for sample in samples if sample.district == district
    ]
    return average_lead(samples_from_district)


assert_equal(average_lead_per_district([], "Appoquinimink"), 0.0)
assert_equal(average_lead_per_district([SAMPLE1], "Appoquinimink"), 2.0)
assert_equal(average_lead_per_district(SAMPLES, "Appoquinimink"), 2.0)
assert_equal(average_lead_per_district(SAMPLES, "Sussex Vo-Tech"), 160.0)

def unique_districts(samples: list[Sample]) -> set[str]:
    districts = [sample.district for sample in samples]
    return set(districts)

def max_lead_average(average_per_district: dict[str, float]) -> str | None:
    result: str | None = None
    largest_average: float = -float("inf")
    for district, average in average_per_district.items():
        if average > largest_average:
            largest_average = average
            result = district
    
    return result

def main():
    # Print average lead for each district in de_school_lead_samples

    samples = convert_lines(de_school_lead_samples)
    
    average_per_district: dict[str, float] = {}

    for district in unique_districts(samples):
        # calculate the average for this specific district (was using the overall average)
        average_per_district[district] = average_lead_per_district(samples, district)
    
    for district, average in average_per_district.items():
        print(f"{district}: {average}")

    # print district with largest average lead level
    district = max_lead_average(average_per_district)
    if district:
        average = average_lead_per_district(samples, district)
        print(f"Max lead is {district}: {average}")

if __name__ == "__main__":
    main()