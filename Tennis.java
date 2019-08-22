import java.util.Scanner;

public class Tennis {

    private static Player2[] players;

    public static void main(String[] args) {

        Scanner s = new Scanner(System.in);
        String input = "a";
        while (!input.equals("q")){
            System.out.println("Would you like to create a new bracket? (y/n)");
            input = s.nextLine();
            if (input.equals("y")) {
                System.out.println("How large of a bracket would you like? (Enter a power of 2)");
                int bracketSize = Integer.parseInt(s.nextLine());
                players = new Player2[bracketSize];
                switch (bracketSize) {
                    case 2:
                        System.out.println("Finals:");
                        break;
                    case 4:
                        System.out.println("Semifinals:");
                        break;
                    case 8:
                        System.out.println("Quarterfinals:");
                        break;
                    default:
                        int x = (int) (Math.log(bracketSize)/Math.log(2));
                        System.out.println("R" + x + ":");
                        break;
                }
                for (int i = 0; i < bracketSize; i++) {
                    System.out.print("Player name: ");
                    String name = s.nextLine();
                    System.out.print("Chance of making it this far (0.XXX): ");
                    double chance = Double.parseDouble(s.nextLine());
                    System.out.print("Win rate against the field (0.XXX): ");
                    double field = Double.parseDouble(s.nextLine());
                    players[i] = new Player2(name, chance, field);
                    System.out.println();
                }
                double[][] rates = new double[bracketSize][bracketSize];
                for (int i = 0; i < bracketSize; i++) {
                    for (int j = i + 1; j < bracketSize; j++) {
                        System.out.print("Chance of " + players[i].name + " beating " + players[j].name + " (0.XXX): ");
                        double chance = Double.parseDouble(s.nextLine());
                        rates[i][j] = chance;
                        rates[j][i] = 1.0 - chance;
                    }
                    System.out.println();
                }
                //printBox(rates);
                while (!input.equals("n")) {
                    System.out.println("\nWhose chance of winning would you like to calculate?");
                    String name = s.nextLine();
                    for (int i = 0; i < bracketSize; i++) {
                        Player2 p = players[i];
                        if (name.equals(p.name)) {
                            System.out.println(name + " has a " + (calculateWin(i, rates) * 100) + "% chance of winning.");
                        }
                    }
                    System.out.println("Would you like to calculate another?");
                    input = s.nextLine();
                }
            }
            System.out.println("Hit 'q' to quit or any key to proceed.");
            input = s.nextLine();
        }
    }

    private static void printBox(double[][] rates) {
        for (double[] x : rates) {
            for (double y : x) {
                System.out.print(String.format("%.2f ", y));
            }
            System.out.println();
        }
    }

    private static double calculateWin(int playerIndex, double[][] rates) {
        int size = rates.length;
        return calculateElse(playerIndex, rates, 0, size);
    }

    private static double calculateElse(int playerIndex, double[][] rates, int low, int high) {
        //System.out.println(playerIndex + " " + low + " " + high + " -> Start of function");
        int size = high - low;
        double chanceSoFar = players[playerIndex].soFar;
        int half = size / 2 + low;
        if (size == 1) {
            return chanceSoFar;
        }
        if (size > 2) {
            if (playerIndex >= low + half) {
                chanceSoFar = calculateElse(playerIndex, rates, half, high);
            } else {
                chanceSoFar = calculateElse(playerIndex, rates, low, half);
            }
        }
        double nonField = 0;
        double runningTotal = 0;
        if (playerIndex >= half) {
            for (int i = low; i < half; i++) {
                double chance = calculateElse(i, rates, low, half);
                nonField += chance;
                runningTotal += chance * rates[playerIndex][i];
            }
        } else {
            for (int i = half; i < high; i++) {
                double chance = calculateElse(i, rates, half, high);
                nonField += chance;
                runningTotal += chance * rates[playerIndex][i];
            }
        }
        double ret = chanceSoFar * (runningTotal + (1-nonField) * (players[playerIndex].rateAgainstField));
        //System.out.println(playerIndex + " " + ret);
        return ret;
    }

    private static class Player2 {
        public String name;
        public double soFar;
        public double rateAgainstField;


        public Player2(String name, double soFar, double rateAgainstField) {
            this.name = name;
            this.soFar = soFar;
            this.rateAgainstField = rateAgainstField;
        }
    }
}

