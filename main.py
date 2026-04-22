energy = {
    "cognitive": 0.8,
    "creative": 0.6,
    "mental": 0.4,
    "physical": 0.2
}

overall_energy = sum(energy.values()) / len(energy)

print(overall_energy)

def energyBar():
    print(f"{round(overall_energy * 50) * "|"}{(99 - round(overall_energy * 100)) * "-"}|")

energyBar()