using Aoc.Shared.Abstract;

namespace Aoc._2024;

public class Day4 : IAocSolution
{
    public int Day => 4;

    private record Board(char[][] Entries)
    {
        public char[][] Entries { get; } = Entries;
        private int _height = Entries.Length;
        private int _width = Entries[0].Length;

        public string WordsFromPosition(int x, int y, int length)
        {
            List<string> words = [];
            for (int i = 0; i < length; i++)
            {
                // Going right
                for 
            }
        }
    }

    public string Part1()
    {
        FilePaths filePaths = new FilePaths();
        var board = new Board(File.ReadAllLines(filePaths.SampleDataPath(4)).Select(line => line.ToArray()).ToArray());
        Console.WriteLine($"Part 1: {board.Entries[0][0]}");
        return "part1";
    }

    public string Part2()
    {
        // FilePaths filePaths = new FilePaths();
        // string instructions = File.ReadAllText(filePaths.InputDataPath(Day)).Replace("\n", "");
        return "part2";
    }
}