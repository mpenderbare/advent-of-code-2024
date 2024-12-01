namespace Aoc.Shared.Abstract;

public class FilePaths
{
    private const string InputDataDir = "/home/pem9cbg/repos/advent-of-code-2024/input";
    private const string SampleDataDir = "/home/pem9cbg/repos/advent-of-code-2024/sample";

    public string InputDataPath(int day)
    {
        var path = Path.Combine(InputDataDir, $"day_{day.ToString()}.txt"); 
        if (!File.Exists(path))
        {
            throw new FileNotFoundException($"Input data file not found at {path}");
        }
        return path;
    }
    
    public string SampleDataPath(int day)
    {
        var path = Path.Combine(SampleDataDir, $"day_{day.ToString()}.txt");
        if (!File.Exists(path))
        {
            throw new FileNotFoundException($"Sample data file not found at {path}");
        }
        return path;
    }
}