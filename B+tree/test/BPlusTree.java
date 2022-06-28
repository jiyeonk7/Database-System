import java.io.*;
import java.util.*;

public class BPlusTree {
    static void argsCheck(String[] args, int num){
        if(args.length != num){
            System.out.printf("WRONG COMMAND");
            System.exit(-1);
        }
    }

    public static void main(String[] args) {
        switch (args[0]){
            case "-c":
                argsCheck(args, 3);
                Create(args[1], Integer.parseInt(args[2]));
                break;

            case "-i":
                argsCheck(args, 3);
                Insert(args[1], args[2]);
                break;

            case "-d":
                argsCheck(args, 3);
                Delete(args[1], args[2]);
                break;

            case "-s":
                argsCheck(args, 3);
                SSearch(args[1], Integer.parseInt(args[2]));
                break;

            case "-r":
                argsCheck(args, 4);
                RSearch(args[1], Integer.parseInt(args[2]), Integer.parseInt(args[3]));
                break;

            default:
                System.exit(-1);
        }
    }

    static void Create(String indexFile, int b){
        BPTree bptree = new BPTree(b);
        saveData(indexFile, bptree);
    }

    static void Insert(String indexFile, String dataFile){
        BPTree bptree = loadTree(indexFile);
        int[][] data = loadData(dataFile);
        int Rows = 0;

        for(int[] row: data) {
            if(bptree.insert(row[0], row[1])){
                Rows++;
            }
        }
        saveData(indexFile, bptree);
    }

    static void Delete(String indexFile, String dataFile){
        BPTree bptree = loadTree(indexFile);
        int[][] data = loadData(dataFile);
        int Rows = 0;

        for (int[] row:data){
            if(bptree.remove(row[0])){
                Rows++;
            }
        }
        saveData(indexFile, bptree);
    }

    static void SSearch(String indexFile, int key){
        BPTree bptree = loadTree(indexFile);

        for (Node node: bptree.search(key).history){
            if (node == null){
                System.out.println("NOT FOUND");
                return;
            }

            else if (node instanceof LeafNode){
                for (Pair<Integer, Integer> pair: ((LeafNode) node).p){
                    if(pair.left == key){
                        System.out.println(pair.right);
                        return;
                    }
                }
                System.out.println("NOT FOUND");
            }

            else{
                StringBuilder message = new StringBuilder();
                int[] keys = node.getKeys();
                for (int i=0; i < keys.length; i++){
                    message.append(keys[i]);
                    if (i != keys.length - 1){
                        message.append(',');
                    }
                }
                System.out.println(message.toString());
            }
        }
    }

    static void RSearch(String indexFile, int startKey, int endKey){
        BPTree bptree = loadTree(indexFile);

        for (Pair<Integer, Integer> pair: bptree.rSearch(startKey, endKey)){
            System.out.printf("%d, %d\n", pair.left, pair.right);
        }
    }

    static int[][] loadData(String fname){
        ArrayList<String> lines = new ArrayList<String>();

        try{
            BufferedReader reader = new BufferedReader(new FileReader(fname));
            while(true){
                String line = reader.readLine();
                if (line == null){
                    break;
                }
                lines.add(line);
            }
            reader.close();
        } catch(IOException e){
            e.printStackTrace();
            return null;
        }

        int[][] array = new int[lines.size()][];

        for (int i =0; i < lines.size(); i++){
            String[] items = lines.get(i).split(",");
            array[i] = new int[items.length];

            for (int j = 0; j < items.length; j++){
                array[i][j] = Integer.parseInt(items[j]);
            }
        }

        return array;
    }

    static void saveData(String fname, BPTree tree){
        try {
            FileOutputStream fileos = new FileOutputStream(fname);
            ObjectOutputStream objectos = new ObjectOutputStream(fileos);
            objectos.writeObject(tree);
            objectos.close();
        } catch (IOException e){
            e.printStackTrace();
        }
    }

    static BPTree loadTree(String fname){
        BPTree result = null;

        try{
            FileInputStream fileis = new FileInputStream(fname);
            ObjectInputStream objectis = new ObjectInputStream(fileis);
            result = (BPTree) objectis.readObject();
            objectis.close();
        } catch (IOException e){
            e.printStackTrace();
        } catch (ClassNotFoundException e){
            e.printStackTrace();
        }

        return result;
    }
}

abstract class Node implements Serializable{
    static final long serialVersionUID = 1L;

    private NonLeafNode parent;

    Node(NonLeafNode parent){
        this.parent = parent;
    }

    public NonLeafNode getParent() {
        return this.parent;
    }

    public void setParent(NonLeafNode node){
        this.parent = node;
    }

    public ArrayList<Node> getSiblings(){
        if(this.parent == null){
            return new ArrayList<>();
        }
        else{
            return this.parent.getChildren();
        }
    }

    public Pair<Node, Node> getNeighbors(){
        Pair<Node, Node> p = new Pair<>(null, null);
        ArrayList<Node> siblings = this.getSiblings();
        int index = siblings.indexOf(this);

        if(index > 0){
            p.left = siblings.get(index-1);
        }

        if(index < siblings.size()-1){
            p.right = siblings.get(index+1);
        }

        return p;
    }

    abstract public int[] getKeys();

    abstract public int getKeyCount();
}

class NonLeafNode extends Node{
    ArrayList<Pair<Integer, Node>> p;
    Node r;
    int m;

    NonLeafNode(NonLeafNode parent){
        super(parent);
        this.r = null;
        this.p = new ArrayList<>();
    }

    @Override
    public int[] getKeys(){
        int[] array = new int[this.p.size()];

        for(int i=0; i < array.length; i++){
            Pair<Integer, Node> pair = this.p.get(i);
            array[i] = pair.left;
        }

        return array;
    }

    @Override
    public int getKeyCount(){
        m = p.size();
        return m;
    }

    public ArrayList<Node> getChildren(){
        ArrayList<Node> array = new ArrayList<>();

        for(Pair<Integer, Node> pair: this.p){
            array.add(pair.right);
        }

        if(this.r != null){
            array.add(this.r);
        }

        return array;
    }

    public int getChildrenCount(){
        int count = this.getKeyCount();

        if(this.r != null){
            ++count;
        }

        return count;
    }

    public void insert(Pair<Integer, Node> pair){
        this.p.add(pair);
        this.p.sort(Comparator.comparingInt(o -> o.left));
    }

    public void insert(int key, Node node){
        this.insert(new Pair<>(key, node));
    }
}

class LeafNode extends Node{
    ArrayList<Pair<Integer,Integer>> p;
    int m;

    LeafNode l;
    LeafNode r;

    LeafNode(NonLeafNode parent){
        super(parent);
        this.l = null;
        this.r = null;
        this.p = new ArrayList<>();
    }

    @Override
    public int[] getKeys(){
        int [] array = new int[this.p.size()];

        for(int i=0; i < array.length; i++){
            Pair<Integer, Integer> pair = this.p.get(i);
            array[i] = pair.left;
        }

        return array;
    }

    @Override
    public int getKeyCount(){
        m = p.size();
        return m;
    }

    public void insert(Pair<Integer,Integer> pair){
        this.p.add(pair);
        this.p.sort(Comparator.comparingInt(o -> o.left));
    }

    public void insert(int key, int value){
        this.insert(new Pair<>(key, value));
    }
}

class Pair<L,R> implements Serializable{
    private static final long serialVersionUID = 1L;

    public L left;
    public R right;

    public Pair(L left, R right){
        this.left = left;
        this.right = right;
    }

    @Override
    public int hashCode(){
        return left.hashCode() ^ right.hashCode();
    }

    @Override
    public boolean equals(Object o){
        if(!(o instanceof Pair)){
            return false;
        }

        Pair pairo = (Pair) o;
        return this.left.equals(pairo.left) && this.right.equals(pairo.right);
    }
}

class BPTree implements Serializable{
    private static final long serialVersionUID = 1L;

    public Node root;
    private int maxChild;

    BPTree(int maxChild){
        this.maxChild = maxChild;
        this.root = new LeafNode(null);
    }

    public ArrayList<Pair<Integer, Integer>> getList(){
        ArrayList<Pair<Integer, Integer>> array = new ArrayList<>();

        Node leftmostN = this.root;
        while(leftmostN instanceof NonLeafNode){
            leftmostN = ((NonLeafNode) leftmostN).p.get(0).right;
        }

        LeafNode leaf = (LeafNode) leftmostN;
        do{
            for(Pair<Integer, Integer> pair: leaf.p){
                array.add(pair);
            }
            leaf = leaf.r;
        } while(leaf != null);

        return array;
    }

    public Boolean insert(int key, int value){
        LeafNode lnode = this.search(key).leaf;

        if (Arrays.binarySearch(lnode.getKeys(), key) >= 0){
            return false;
        }

        insertValue(key, value, lnode);
        return true;
    }

    private void insertValue(int key, int value, LeafNode lnode){
        lnode.insert(key, value);

        if(lnode.getKeyCount() > this.maxChild){
            splitNode(lnode);
        }
    }

    private void splitNode(Node node){
        Node newN = null;

        if(node == this.root){
            this.root = new NonLeafNode(null);
            node.setParent((NonLeafNode) this.root);
            ((NonLeafNode) this.root).r = node;
        }

        if(node instanceof LeafNode){
            newN = new LeafNode(node.getParent());
            ((LeafNode) newN).p = new ArrayList<>(((LeafNode) node).p.subList(0,(node.getKeyCount()+1)/2));
            ((LeafNode) node).p = new ArrayList<>(((LeafNode) node).p.subList((node.getKeyCount()+1)/2, node.getKeyCount()));

            if(((LeafNode) node).l != null){
                ((LeafNode) node).l.r = ((LeafNode) newN);
            }
            ((LeafNode) newN).l = ((LeafNode) node).l;
            ((LeafNode) newN).r = ((LeafNode) node);
            ((LeafNode) node).l = ((LeafNode) newN);
        }

        else if(node instanceof NonLeafNode){
            newN = new NonLeafNode(node.getParent());
            ((NonLeafNode) newN).p = new ArrayList<>(((NonLeafNode) node).p.subList(0, (node.getKeyCount()+1)/2));
            ((NonLeafNode) node).p = new ArrayList<>(((NonLeafNode) node).p.subList((node.getKeyCount()+1)/2, node.getKeyCount()));

            for(Node child: ((NonLeafNode) newN).getChildren()){
                child.setParent((NonLeafNode) newN);
            }
        }

        insertNode(newN, node, node.getParent());

        if(node.getParent().getKeyCount() >= this.maxChild){
            splitNode(node.getParent());
        }
    }

    private void insertNode(Node leftN, Node rightN, NonLeafNode parentN){
        Node leftmostofRightN = rightN;

        while(leftmostofRightN instanceof NonLeafNode){
            leftmostofRightN = ((NonLeafNode) leftmostofRightN).p.get(0).right;
        }

        int key = leftmostofRightN.getKeys()[0];
        parentN.insert(key, leftN);
    }

    public Boolean remove(int key){
        LeafNode node = this.search(key).leaf;
        int index = Arrays.binarySearch(node.getKeys(), key);

        if (index < 0){
            return false;
        }

        deleteValue(key, node);
        return true;
    }

    private void deleteValue(int key, LeafNode node){
        int index = Arrays.binarySearch(node.getKeys(), key);
        node.p.remove(index);

        if(node.getKeyCount() < (this.maxChild-1)/2 && node != this.root){
            balanceNode(node);
        }
    }

    private void balanceNode(Node node){
        Pair<Node, Node> neighbor = node.getNeighbors();

        if(neighbor.right != null && neighbor.right.getKeyCount()+node.getKeyCount() < this.maxChild){
            merge(node, neighbor.right, node.getParent());
        }

        else if(neighbor.left != null && neighbor.left.getKeyCount()+node.getKeyCount() < this.maxChild){
            merge(neighbor.left, node, node.getParent());
        }

        else{
            if(neighbor.right != null){
                if(node instanceof LeafNode){
                    ((LeafNode) node).insert(((LeafNode) neighbor.right).p.remove(0));
                }
                else{
                    ((NonLeafNode) node).insert(((NonLeafNode) neighbor.right).p.remove(0));
                }

                updateKey(node.getParent(), node, neighbor.right);
            }

            else if(neighbor.left != null){
                if(node instanceof LeafNode){
                    ((LeafNode) node).insert(((LeafNode) neighbor.left).p.remove(neighbor.left.getKeyCount()-1));
                }
                else{
                    ((NonLeafNode) node).insert(((NonLeafNode) neighbor.left).p.remove(neighbor.left.getKeyCount()-1));
                }

                updateKey(node.getParent(), neighbor.left, node);
            }
        }
    }

    private void merge(Node leftN, Node rightN, NonLeafNode parentN){
        if(leftN instanceof LeafNode){
            for(Pair<Integer, Integer> pair:((LeafNode) leftN).p){
                ((LeafNode) rightN).insert(pair);
            }
        }

        else if(leftN instanceof NonLeafNode){
            for(Pair<Integer, Node> pair: ((NonLeafNode) leftN).p){
                ((NonLeafNode) rightN).insert(pair);
            }
        }

        for(int i = 0; i < parentN.p.size(); i++){
            if(parentN.p.get(i).right == leftN){
                parentN.p.remove(i);

                if(leftN instanceof LeafNode){
                    LeafNode leftleftN = ((LeafNode) leftN).l;
                    if(leftleftN != null){
                        leftleftN.r = (LeafNode) rightN;
                    }
                    ((LeafNode) rightN).l = leftleftN;
                }
                break;
            }
        }

        if(parentN == this.root && parentN.getChildrenCount() == 1){
            rightN.setParent(null);
            this.root = rightN;
            return;
        }

        if(parentN.getKeyCount() < this.maxChild/2){
            balanceNode(parentN);
        }
    }

    private void updateKey(NonLeafNode parentN, Node leftN, Node rightN){
        Node leftmostofRightN = rightN;
        while(leftmostofRightN instanceof NonLeafNode){
            leftmostofRightN = ((NonLeafNode) leftmostofRightN).p.get(0).right;
        }

        int key = leftmostofRightN.getKeys()[0];

        for(Pair<Integer, Node> pair: parentN.p){
            if(pair.right == leftN){
                pair.left = key;
                break;
            }
        }
    }

    public SearchResult search(int key){
        ArrayList<Node> history = new ArrayList<>();
        LeafNode leaf = searchProc(key, this.root, history);

        if(leaf == null){
            return SearchResult.miss(leaf, history);
        }

        for(Pair<Integer, Integer> pair: leaf.p){
            if(pair.left == key){
                return SearchResult.hit(pair.right, leaf, history);
            }
        }
        return SearchResult.miss(leaf, history);
    }

    private LeafNode searchProc(int key, Node node, ArrayList<Node> history){
        if(history != null){
            history.add(node);
        }

        if(node == null){
            return null;
        }

        else if (node instanceof LeafNode){
            return (LeafNode) node;
        }

        else{
            for(Pair<Integer, Node> pair: ((NonLeafNode) node).p){
                if(key < pair.left){
                    return searchProc(key, pair.right, history);
                }
            }
            return searchProc(key, ((NonLeafNode) node).r, history);
        }
    }

    public ArrayList<Pair<Integer, Integer>> rSearch(int startKey, int endKey){
        ArrayList<Pair<Integer, Integer>> array = new ArrayList<>();

        for(LeafNode leaf: rSearchProc(startKey, endKey, this.root)){
            for(Pair<Integer, Integer> pair: leaf.p){
                if(pair.left >= startKey && pair.left <= endKey){
                    array.add(pair);
                }
            }
        }

        return array;
    }

    private ArrayList<LeafNode> rSearchProc(int startKey, int endKey, Node node) {
        ArrayList<LeafNode> leafArray = new ArrayList<>();

        if (node == null) {
            return leafArray;
        }

        if (node instanceof LeafNode) {
            leafArray.add((LeafNode) node);
        } else {
            for (Pair<Integer, Node> pair : ((NonLeafNode) node).p) {
                if (startKey < pair.left) {
                    leafArray.addAll(rSearchProc(startKey, endKey, pair.right));
                }
            }

            if (node.getKeys()[node.getKeyCount() - 1] <= endKey) {
                leafArray.addAll(rSearchProc(startKey, endKey, ((NonLeafNode) node).r));
            }
        }

        return leafArray;
    }
}


class SearchResult{
    boolean hit;
    int value;
    LeafNode leaf;
    ArrayList<Node> history;

    SearchResult(boolean hit, int value, LeafNode leaf, ArrayList<Node> history){
        this.hit = hit;
        this.value = value;
        this.leaf = leaf;
        this.history = history;
    }

    static SearchResult hit(int value, LeafNode leaf, ArrayList<Node> history){
        return new SearchResult(true, value, leaf, history);
    }

    static SearchResult miss(LeafNode leaf, ArrayList<Node> history){
        return new SearchResult(false, -1, leaf, history);
    }
}