using System.Text.RegularExpressions;
using Aoc.Shared.Abstract;

namespace Aoc._2024;

public class Day3 : IAocSolution
{
    public int Day => 3;
    
    public string Part1()
    {
        FilePaths filePaths = new FilePaths();
        string instructions = File.ReadAllText(filePaths.InputDataPath(Day)).Replace("\n", "");
        string pattern = @"mul\((\d{1,3}),(\d{1,3})\)";
        Regex regex = new Regex(pattern);
        MatchCollection matches = regex.Matches(instructions);

        int total = 0;
        foreach (Match match in matches)
        {
            total += int.Parse(match.Groups[1].Value) * int.Parse(match.Groups[2].Value);
        }
        return total.ToString();
    }

    private (string instruction, string remaining) ExtractInstruction(string instructions, bool enabled)
    {
        string delimiter = enabled ? @"don't\(\)" : @"do\(\)";
        Match match = Regex.Match(instructions, delimiter);
        if (match.Success)
        {
            string before = instructions.Substring(0, match.Index);
            string after = instructions.Substring(match.Index + match.Length);
            return (before, after);
        }
        
        return (instructions, string.Empty);
    }

    private List<string> ExtractEnabledInstructions(string instructions)
    {
        bool enabled = true;
        string remainingInstructions = instructions;
        List<string> enabledInstructions = [];
        while (remainingInstructions.Length > 0)
        {
            (string before, string after) = ExtractInstruction(remainingInstructions, enabled);
            if (enabled) enabledInstructions.Add(before);
            remainingInstructions = after;
            enabled = !enabled;    
        }
        return enabledInstructions;

    }

    public string Part2()
    {
        FilePaths filePaths = new FilePaths();
        string instructions = File.ReadAllText(filePaths.InputDataPath(Day)).Replace("\n", "");
        string enabledInstructions = String.Join("", ExtractEnabledInstructions(instructions));
        
        string pattern = @"mul\((\d{1,3}),(\d{1,3})\)";
        Regex regex = new Regex(pattern);
        MatchCollection matches = regex.Matches(enabledInstructions);

        int total = 0;
        foreach (Match match in matches)
        {
            total += int.Parse(match.Groups[1].Value) * int.Parse(match.Groups[2].Value);
        }
        
        return total.ToString();
    }
}