opt = {
    path_csv = 'download/danbooru-targets.csv',
    path_result = '/media/paulo/DADOS/coco_icml_train2017_vFinal_Lua/'
}

-- one-line argument parser. parses enviroment variables to override the defaults
for k,v in pairs(opt) do opt[k] = tonumber(os.getenv(k)) or os.getenv(k) or opt[k] end
print(opt)

csv = require("csv")
f = csv.open(opt.path_csv)
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{} "
dict = {}
for i = 1,#alphabet do
    dict[alphabet:sub(i,i)] = i
end
i=0
for fields in f:lines() do
        imagepath = fields[1]
        tags = fields[2]
        converted = torch.ByteTensor(201,5):zero()
        converted2 = torch.FloatTensor(5,1024):zero()
        for j = 1,math.min(201,#tags) do
            encoded = dict[tags:sub(j,j)]
            if encoded == nil then
                converted[j] = 0
            else
                converted[j] = encoded
            end
        end    
        x = { txt=converted2, img=imagepath, char=converted }
        torch.save(opt.path_result..string.format(i)..".t7", x)
        i=i+1
end