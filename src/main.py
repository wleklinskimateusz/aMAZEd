from generator.generator import Generator


def main() -> None:
    generator_algorithms: list[type[Generator]] = []
    for GeneratorClass in generator_algorithms:
        generator = GeneratorClass(10, 10)
        maze = generator.generate()
        print(maze)


if __name__ == "__main__":
    main()
