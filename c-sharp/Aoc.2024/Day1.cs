using Aoc.Shared.Abstract;

namespace Aoc._2024;

public class Day1 : IAocSolution
{
    public int Day => 1;

    private (int[], int[]) GetValues()
    {
        var filePaths = new FilePaths();
        var values = File.ReadAllLines(filePaths.InputDataPath(Day)).Select(line => line.Split(' ', StringSplitOptions.RemoveEmptyEntries)).ToArray();
        var lefts = values.Select(pair => int.Parse(pair[0])).Order().ToArray();
        var rights = values.Select(pair => int.Parse(pair[1])).Order().ToArray();
        
        return (lefts, rights);
    }

    public string Part1()
    {
        var (lefts, rights) = GetValues();
        int result = lefts.Zip(rights, (left, right) => Math.Abs(left - right)).Sum();

        return result.ToString();
    }

    public string Part2()
    {
        var (lefts, rights) = GetValues();
        var result = lefts.Sum(left => left * rights.Count(right => right == left));
        return result.ToString();
    }

}