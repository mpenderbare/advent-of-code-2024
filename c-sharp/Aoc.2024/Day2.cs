using Aoc.Shared.Abstract;

public class Day2 : IAocSolution
{
    public int Day => 2;

    private List<List<int>> GetReports()
    {
        var filePaths = new FilePaths();
        var reports = File.ReadAllLines(filePaths.InputDataPath(Day)).Select(line => line.Split(' ', StringSplitOptions.RemoveEmptyEntries).Select(level => int.Parse(level)).ToList()).ToList();
        return reports;
    }

    private bool IsIncreasing(List<int> report)
    {
        for (int i = 0; i < report.Count - 1; i++)
        {
            if (report[i] > report[i + 1]) return false;
        }
        return true;
    }

    private bool IsDecreasing(List<int> report)
    {
        for (int i = 0; i < report.Count - 1; i++)
        {
            if (report[i] < report[i + 1]) return false;
        }
        return true;
    }

    private bool LevelsClose(List<int> report)
    {
        for (int i = 0; i < report.Count - 1; i++)
        {
            var diff = Math.Abs(report[i] - report[i + 1]);
            if ((diff < 1) || (diff > 3)) return false;
        }
        return true;
    }

    private bool IsSafe(List<int> report)
    {
        return (IsDecreasing(report) || IsIncreasing(report)) && LevelsClose(report);
    }
    
    public string Part1()
    {
        var reports = GetReports();
        return reports.Count(report => IsSafe(report)).ToString();
    }

    private IEnumerable<List<int>> GetReducedReports(List<int> report)
    {
        for (int i = 0; i < report.Count; i++)
        {
            var reducedReport = new List<int>(report);
            reducedReport.RemoveAt(i);
            yield return reducedReport;
        }
    }
    
    private bool ExistsSafeSubreport(List<int> report)
    {
        foreach (var reducedReport in GetReducedReports(report))
        {
            if (IsSafe(reducedReport)) return true;
        }
        
        return false;
    }

    public string Part2()
    {
        var safeReports = 0; 
        foreach (var report in GetReports())
        {
            if (IsSafe(report)) safeReports++;
            else if (ExistsSafeSubreport(report)) safeReports++;
        }

        return safeReports.ToString();
    }

}