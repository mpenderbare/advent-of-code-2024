using Aoc.Shared.Abstract;

public class Day1 : IAocSolution
{
    public int Day => 1;
    private static FilePaths _filePaths = new FilePaths();
    private static readonly string InputPath = _filePaths.InputDataPath(1);
    private static readonly string SamplePath = _filePaths.SampleDataPath(1);

    private (int[], int[]) GetValues()
    {
        var values = File.ReadAllLines(InputPath).Select(line => line.Split(' ', StringSplitOptions.RemoveEmptyEntries));
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